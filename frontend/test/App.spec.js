import {test, expect} from 'vitest';
import {mount} from '@vue/test-utils';
import sinon from 'sinon';

import {createRouter, createWebHistory} from 'vue-router';

import App from '../src/App.vue';
import Navigation from '../src/components/NavigationComponent.vue';
import AnalysisListingView from '../src/views/AnalysisListingView.vue';
import AnalysisCreateView from '../src/views/AnalysisCreateView.vue';
import AboutView from '../src/views/AboutView.vue';

// Skipping these tests due to the use of Vue Router.
// Running test without mocking result in following warnings:
// [Vue warn]: Failed to resolve component: router-view
// [Vue warn]: Failed to resolve component: router-link
// https://www.wrike.com/open.htm?id=837264942
test.skip('Vue instance exists and it is an object', () => {
  const mockRouter = {
    push: sinon.stub(),
  };

  const wrapper = mount(App, {
    shallow: false,
    global: {
      mocks: {
        $router: mockRouter,
      },
    },
  });

  console.log(wrapper);

  expect(1).toBe(1);
});

test.only('Using a real router!', () => {
  const router = createRouter({
    history: createWebHistory(),
    routes: [
      {
        path: '/',
        component: AnalysisListingView,
      },
      {
        path: '/analysis/create',
        component: AnalysisCreateView,
      },
      {
        path: '/about',
        component: AboutView,
      },
    ],
  });

  console.log(router);

  const wrapper = mount(App, {
    global: {
      plugins: [router],
    },
  });

  console.log(wrapper.html());
});

test.skip('Contains a <sidebar> tag with a <navigation> component', () => {
  const wrapper = mount(App, {shallow: true});

  expect(wrapper.find('app-sidebar').exists()).toBe(true);

  const sidebarNavComponent = wrapper.findComponent(Navigation);

  expect(sidebarNavComponent).toBeTruthy;
});
