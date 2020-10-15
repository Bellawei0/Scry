// src/components/Register.jsx
import React, { Component } from "react";
import axios from "axios";
import Alert from "./Alert";
import "./Login.css";

class Login extends Component {
    state = { err: "" };
    login = (e) => {
        e.preventDefault();
        axios
            .post("http://127.0.0.1:5000/api/login", {
                email: document.getElementById("email").value,
                pwd: document.getElementById("password").value,
            })
            .then((res) => {
                if (res.data.error) {
                    this.setState({ err: res.data.error });
                } else {
                    this.setState({ login: true });
                }
            });
    };

        render() {
        return (
            <div className="grandParentContaniner">
                <div className="parentContainer">
                    <form onSubmit={this.login}>
                        <h1>Welcome to Scry</h1>
                        <div className="inset">
                        <p>
                            <label htmlFor="email">EMAIL ADDRESS</label>
                            <input
                                type="text"
                                name="email"
                                id="email"
                            />
                        </p>
                        <p>
                            <label htmlFor="password">PASSWORD</label>
                            <input
                                type="password"
                                name="password"
                                id="password"
                            />
                        </p>
                        <div className="forgot">
                <a href="reset_password" style={{color: '#0d93ff'}}>Forgot Password?</a>
              </div>
                        <p>
                            <button type="submit">
                                Sign In
                            </button>
                            {this.state.login && <p>You're logged in!</p>}
                        </p>
                        <p className="signUp">
                Dont have an account? <a href="sign_up" style={{color: '#0d93ff'}}>SIGN UP</a>
              </p>
                        </div>
                    </form>
                    {this.state.err.length > 0 && (
                        <Alert
                            message={`Check your form and try again! (${this.state.err})`}
                        />
                    )}
                </div>
            </div>
        );
    }
}

export default Login;
