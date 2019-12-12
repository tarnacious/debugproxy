/* @flow */

declare var jest: any;
declare var it: (name: string, body: () => any) => any;
declare var describe: (name: string, body: () => any) => any;
declare var expect: (x: any) => any;
declare var beforeEach: (x: any) => any;

jest.unmock('../Footer');

import React from 'react';
import ReactDOM from 'react-dom';
import TestUtils from 'react-addons-test-utils';
import {FooterComponent} from 'components/Header/Footer';


describe('Footer', () => {
    var footerComponent;

    beforeEach(function() {
      footerComponent = TestUtils.renderIntoDocument(
          <FooterComponent />
      );
    })

    it('renders footer text', () => {
      const elem = TestUtils.findRenderedDOMComponentWithClass(footerComponent, "footer");
      expect(elem.textContent).toEqual('Footer');
    });
});
