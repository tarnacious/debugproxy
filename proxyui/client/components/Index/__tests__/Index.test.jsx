/* @flow */

declare var jest: any;
declare var it: (name: string, body: () => any) => any;
declare var describe: (name: string, body: () => any) => any;
declare var expect: (x: any) => any;
declare var beforeEach: (x: any) => any;

jest.unmock('../Index.jsx');

import React from 'react';
import ReactDOM from 'react-dom';
import TestUtils from 'react-addons-test-utils';

import { shallow } from 'enzyme';
import { IndexComponent } from 'components/Index/Index';
import Header from 'components/Header/Header';
import Footer from 'components/Header/Footer';

describe('IndexComponent', () => {


  describe("with user", () => {

    var component;

    beforeEach(function() {
      component = shallow(<IndexComponent dispatch={ null } />)
    })

    it('should render header component', () => {
      expect(component.find(Header).length).toEqual(1)
    });

    it('should render footer component', () => {
      expect(component.find(Footer).length).toEqual(1)
    });

  });


});
