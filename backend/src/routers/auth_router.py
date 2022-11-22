""" FastAPI Authentication router file that handles the auth lifecycle of the application """
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from cas import CASClient

from ..config import Settings, get_settings
from ..dependencies import database
from ..models.user import User, VerifyUser
from ..security.security import authenticate, create_access_token, get_authorization, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(database)],
)

# URLs for interacting with UAB CAS Padlock system for BlazerID
cas_client = CASClient(
    version=3,
    service_url=get_settings().cas_api_service_url,
    server_url=get_settings().cas_server_url,
)


## Test Route ##
@router.get("/dev_only_test")
def test(authorized=Security(get_authorization, scopes=["developer"])):
    """ Only developers can hit this endpoint """
    print(authorized)
    return {
        "Ka": ["Boom", "Blammo", "Pow"],
    }


# pylint: disable=no-member
# This is done because pylint doesn't appear to be recognizing python-cas's functions saying they have no member
@router.get("/login")
async def login(
    response: Response,
    nexturl: Optional[str] = None,  # CAS Nexturl
    ticket: Optional[str] = None,
    repositories=Depends(database),
    settings: Settings = Depends(get_settings),
):
    """Rosalution Login Method"""
    if not ticket:
        # No ticket, the request comes from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        return {"url": cas_login_url}

    # These are returned by UAB CAS login, but they are unused beyond the user value
    # pylint: disable=unused-variable
    cas_user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    if not cas_user:
        print("Failed Padlock ticket user verification, redirect back to login page")
        # Failed ticket verification, this should be an error page of some kind maybe?

        redirect_frontend_route_response = settings.web_base_url + settings.auth_web_failure_redirect_route
        return RedirectResponse(redirect_frontend_route_response)

    # Login was successful, redirect to the 'nexturl' query parameter
    user = repositories["user"].find_by_username(cas_user)
    user_authenticated = authenticate(user, 'secret')

    if not user_authenticated:
        raise HTTPException(status_code=401, detail="Unauthorized Rosalution user")

    data_to_encode = {
        "sub": user_authenticated['username'],
        "scopes": [user_authenticated['scope']],
    }
    access_token = create_access_token(
        data_to_encode, settings.oauth2_access_token_expire_minutes, settings.rosalution_key, settings.oauth2_algorithm
    )

    response = RedirectResponse(url=settings.web_base_url + nexturl)
    response.delete_cookie(key="rosalution_TOKEN")
    response.set_cookie(key="rosalution_TOKEN", value=access_token)

    return response


# This needs to be /token for the api/docs to work in issuing and recognizing a bearer
@router.post("/token", response_model=User)
def login_local_developer(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    repositories=Depends(database),
    settings: Settings = Depends(get_settings),
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = repositories["user"].find_by_username(form_data.username)
    user_authenticated = authenticate(user, form_data.password)

    if not user_authenticated:
        raise HTTPException(status_code=401, detail="Unauthorized Rosalution user")

    data_to_encode = {
        "sub": user_authenticated['username'],
        "scopes": [user_authenticated['scope']],
    }
    access_token = create_access_token(
        data_to_encode, settings.oauth2_access_token_expire_minutes, settings.rosalution_key, settings.oauth2_algorithm
    )

    content = {"access_token": access_token, "token_type": "bearer"}
    response = JSONResponse(content=content)
    response.delete_cookie(key='rosalution_TOKEN')
    response.set_cookie(key="rosalution_TOKEN", value=access_token)

    return response


@router.get("/verify_token", response_model=User)
def verify_token(
    repositories=Depends(database),
    username: VerifyUser = Security(get_current_user),
):
    """This function issues the authentication token for the frontend to make requests"""
    user = repositories["user"].find_by_username(username)
    current_user = User(**user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")

    return current_user


@router.get("/logout")
def logout_oauth(request: Request, response: Response, settings: Settings = Depends(get_settings)):
    """ Destroys the session and determines if the request was local or production and returns the proper url """

    content = {"access_token": ""}

    if settings.cas_login_enable:
        redirect_url = request.url_for("logout_callback")
        cas_logout_url = cas_client.get_logout_url(redirect_url)
        content = {"url": cas_logout_url}

    response = JSONResponse(content=content)
    response.delete_cookie(key="rosalution_TOKEN")

    return response


@router.get('/logout_callback')
def logout_callback(settings: Settings = Depends(get_settings)):
    """
    The endpoint that gets called after the production logout function is called and redirects
    back to the login page
    """
    redirect_url = settings.web_base_url + settings.auth_web_failure_redirect_route
    return RedirectResponse(url=redirect_url)
