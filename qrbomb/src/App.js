import React, { Component } from 'react';
import { Container, Jumbotron, FormGroup, Label, Input, Button } from 'reactstrap';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  bomb() {

  }
  render() {
    return (
      <div className="App flexbox-row">
        <div className="flexbox-column">
          <h1 id="title" className="my-5">1 Click Bomb</h1>
          <FormGroup>
            <Label for="exampleText" className="label">Message</Label>
            <Input type="textarea" name="text" id="exampleText" />
          </FormGroup>
          <Button onClick={this.bomb}>Bomb</Button>
        </div>
      </div>
    );
  }
}

export default App;
