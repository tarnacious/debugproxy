/* @flow */

import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { connect } from 'react-redux'

import { prettyUrl, truncate } from 'lib/utils';
import { changeQuery } from 'actions/filter';
import type Action from 'types/action';
import type State from 'types/state';
import Input from 'components/Input/Input';


export class FilterComponent extends Component {

  props: Props;

  onChange(e : SyntheticInputEvent) {
    this.props.dispatch(changeQuery(e.target.value));
  }

  onKeyPress(e) {
    if (e.key == "Escape") {
      ReactDOM.findDOMNode(this).querySelector('input').blur();
      return;
    }
    if (e.key == "Enter") {
      ReactDOM.findDOMNode(this).querySelector('input').blur();
      return;
    }
  }

  render() {
    return (
      <div className="filters">
        <Input placeholder="Filter Request List"
          onKeyDown={ (e) => this.onKeyPress(e) }
          onChange={ (e) => this.onChange(e) }
          value={ this.props.query }
        />
      </div>
    )
  }
}


type Props = {
  query: string,
  dispatch: Action
};

function mapStateToProps(state: State) {
  return {
    query: state.filter.query
  }
}

export default connect(mapStateToProps)(FilterComponent);
