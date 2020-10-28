import React from "react";
import Axios from "axios";

class Forecast extends React.Component {
    state = {graphURL: "hello", isLoading: true}

    componentDidMount()
    {
    	Axios.get("/api/forecast",{
            headers:
            {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        }).then(res =>
    	{
    		//this.setState({graphURL: res.data})
    		this.setState({isLoading: false})
    	})
    }

    render(){
    	const {graphURL, isLoading} = this.state;
    	if(isLoading)
    	{
    		return <div className="App">Loading...</div>;
    	}

    	return (
        <React.Fragment>
            <div className="w3-container w3-center" style={{margin: "3rem"}}>
                <h1 className="w3-jumbo">{String(this.state.isLoading)}</h1>
                <button type="button" className="w3-button w3-blue" onClick={() => window.location = "/"}>&laquo; Back</button>
            </div>
        </React.Fragment>
        );
        }
}

export default Forecast;