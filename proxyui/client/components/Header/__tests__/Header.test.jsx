/* @flow */

declare var jest: any;
declare var it: (name: string, body: () => any) => any;
declare var describe: (name: string, body: () => any) => any;
declare var expect: (x: any) => any;
declare var beforeEach: (x: any) => any;


jest.unmock('../Header');
import React from 'react';
import ReactDOM from 'react-dom';
import TestUtils from 'react-addons-test-utils';
import {HeaderComponent} from 'components/Header/Header';


describe('Header', () => {

    var headerComponent;

    beforeEach(function() {
      headerComponent = TestUtils.renderIntoDocument(
          <HeaderComponent />
      );
    })

    it('renders header text', () => {
      const elem = TestUtils.findRenderedDOMComponentWithClass(headerComponent, "header");
      expect(elem.textContent).toEqual('Header');
    });

});
