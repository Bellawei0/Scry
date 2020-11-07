import React from "react";
import Axios from "axios";
import Popup from "./Popup";


function deleteProduct(pid)
{
    Axios.delete("/api/deleteproduct/" + pid, {headers: { Authorization: "Bearer " +localStorage.getItem("token") }}).then(res => {
    console.log(res.data)
    window.location.reload();
    })
}
class DataItem extends React.Component 
{
    constructor(props) 
    {
      super(props);

      this.state = 
      {
      };
  }
    render(){
    return (
        <div
            className="w3-card w3-border w3-border-gray w3-round-large"
            style={{ marginTop: "2rem" }}>
            <header className="w3-container w3-opacity w3-light-gray" style={{padding: "1rem"}}>Owner: @{this.props.author}</header>
            <h1>{this.props.title}</h1>
            <Popup id= {this.props.id}/>
            <div className="w3-container" style={{ padding: "2rem" }}>
                <h2 className="w3-xxlarge">
                    {this.props.isOwner &&
                    <button className="w3-right w3-button w3-red w3-large w3-hover-pale-red w3-round-large" onClick={() => deleteProduct(this.props.id)}>Delete                    
                    </button>}
                    <button className="w3-right w3-button w3-red w3-large w3-hover-pale-red w3-round-large" onClick={() => {
                        document.getElementById("popup").style.display = "block"
                    }}>Get Forecast</button>
                </h2>
                <div dangerouslySetInnerHTML={{__html: this.props.content}}/>
            </div>
        </div>
    );
}
}
export default DataItem;