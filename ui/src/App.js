import logo from './logo.svg';
import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import { createContext, useContext, useState } from 'react';
import { act } from 'react-dom/test-utils';
import { Form, Button, Container } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import axios from "axios";

const UserContext = createContext();

function App() {
  const [expectedAnswer, setExpectedAnswer] = useState("");
  const [actualAnswer, setActualAnswer] = useState("");
  const [result, setResult] = useState("No result yet");
  const onChangeExpectedAnswer = (e) => {
    setExpectedAnswer(e.target.value);
  }
  const onChangeActualAnswer = (e) => {
    setActualAnswer(e.target.value);
  }
 const submitAnswer = async (e) => {
   e.preventDefault();
  setResult("Loading.....");
  const response = await axios.post('http://127.0.0.1:5000/process', {expectedAnswer: expectedAnswer, actualAnswer: actualAnswer});
  setResult("Score = "+(response.data*100).toFixed(2));
  }

return (
    <div className="App">
<Container>
<div><h1>Score estimater</h1></div>
<Form>
  <Form.Group className="mb-3" controlId="formEA">
    <Form.Label>Teachers Answer</Form.Label>
    <Form.Control as="textarea" rows={3} placeholder="Teachers Answer" onChange={onChangeExpectedAnswer}/>
  </Form.Group>
  <Form.Group className="mb-3" controlId="formAA">
    <Form.Label>Students Answer</Form.Label>
    <Form.Control as="textarea" rows={3} placeholder="Students Answer" onChange={onChangeActualAnswer}/>
  </Form.Group>

  <Button variant="primary" type="submit" onClick={submitAnswer}>
    Submit
  </Button>
</Form>
<div class="container">
  <h4>{result}</h4>
</div>
</Container>

       
    </div>
  );
}

export default App;
