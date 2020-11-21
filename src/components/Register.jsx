// src/components/Register.jsx
import React, { Component } from "react";
import axios from "axios";
import Alert from "./Alert";

class Register extends Component {
  state = { err: "" };
  register = (e) => {
    e.preventDefault();
    axios
      .post("/api/register", {
        email: document.getElementById("email").value,
        username: document.getElementById("username").value,
        pwd: document.getElementById("password").value,
      })
      .then((res) => {
        if (res.data.error) {
          this.setState({ err: res.data.error });
        } else {
          window.location = "/login";
        }
      });
  };

  render() {
    return (
      <div class="showcase">
        <div className="grandParentContaniner">
          <div class="w3-cell-row">
            <div class="w3-third w3-container w3-Deep Purple">
              <p></p>
            </div>

            <div class="w3-third w3-container w3-black">
              <div className="w3-card-4" style={{ margin: "2rem" }}>
                <div className="w3-container w3-black w3-center w3-xlarge">
                  <h1 className="w3-center">REGISTER</h1>
                </div>
                <div className="w3-container">
                  {this.state.err.length > 0 && (
                    <Alert
                      message={`Check your form and try again! (${this.state.err})`}
                    />
                  )}
                  <form onSubmit={this.register}>
                    <p>
                      <label htmlFor="email">Email</label>
                      <input
                        type="email"
                        class="w3-input w3-border"
                        id="email"
                      />
                    </p>
                    <p>
                      <label htmlFor="username">Username</label>
                      <input
                        type="text"
                        class="w3-input w3-border"
                        id="username"
                      />
                    </p>
                    <p>
                      <label htmlFor="password">Password</label>
                      <input
                        type="password"
                        class="w3-input w3-border"
                        id="password"
                      />
                    </p>
                    <p>
                      <button type="submit" class="w3-button w3-blue">
                        Register
                      </button>
                    </p>
                  </form>
                </div>
              </div>
            </div>
          </div>
          <div>
            <img
              className="mx-auto rounded-circle"
              src={require("./assets/img/space.jpg")}
              alt=""
            />
            <h1>hele</h1>
          </div>
        </div>
      </div>
    );
  }
}

export default Register;
