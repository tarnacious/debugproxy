/* @flow */

declare var jest: any;
declare var it: (name: string, body: () => any) => any;
declare var describe: (name: string, body: () => any) => any;
declare var expect: (x: any) => any;

jest.dontMock('reducers');

describe('user', () => {
  const user = require('reducers').user;

  it('defaults to not connected', function() {
    //expect(user(undefined, {})).toEqual({'connected': false});
  });

  it('can be connected', function() {
    expect(user(undefined, {'type': 'CONNECT'})).toEqual({'connected': true});
  });

  it('can be disconnected', function() {
    expect(user(undefined, {'type': 'DISCONNECT'})).toEqual({'connected': false});
  });

});
