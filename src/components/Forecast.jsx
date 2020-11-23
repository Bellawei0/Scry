import React from "react";
import Axios from "axios";
import { JsonToTable } from "react-json-to-table";

class Forecast extends React.Component 
{
  state = {
    graphURL: "hello",
    isLoading: true,
    responsey: "",
  };

    componentDidMount()
    {
        const params = new URLSearchParams(window.location.search)
        const foo = params.get('id')
        const bar = params.get('length')
      Axios.get("/api/forecast?id=" + foo + "&length=" + bar,
        {
            headers:
            {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }).then(res =>
      {
        this.setState({graphURL: (res.data.success)})
            delete res.data.success;
        this.setState({responsey: (res.data), isLoading: false})
      })
    }

  render() {
    const { graphURL, isLoading } = this.state;
    if (isLoading) {
      return <div className="App">Loading...</div>;
    }

    return (
      <React.Fragment>
        <div
          className="w3-container w3-light-grey w3-center"
          style={{ margin: "3rem" }}
        >
          <h1 className="w3-jumbo">{this.state.isLoading}</h1>
          <img alt="derp" src={this.state.graphURL} />
          <JsonToTable json={this.state.responsey} />
          <button
            type="button"
            className="w3-button w3-blue"
            onClick={() => (window.location = "/")}
          >
            &laquo; Back
          </button>
        </div>
      </React.Fragment>
    );
  }
}

export default Forecast;
