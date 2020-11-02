import React from "react";
import Axios from "axios";
import Modal from "./Modal";
import Popup from "./Popup";


function deleteTweet(tid)
{
    Axios.delete("/api/deletetweet/" + tid, {headers: { Authorization: "Bearer " +localStorage.getItem("token") }}).then(res => {
    console.log(res.data)
    window.location.reload();
    })
}
class TweetItem extends React.Component 
{
    constructor(props) {
    super(props);

    this.state = {
      modal: false,
      name: "",
      modalInputName: ""
    };
  }
  handleChange(e) {
    const target = e.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  }

  handleSubmit(e) {
    this.setState({ name: this.state.modalInputName });
    this.modalClose();
  }

  modalOpen() {
    this.setState({ modal: true });
  }

  modalClose() {
    this.setState({
      modalInputName: "",
      modal: false
    });
  }
    render(){
    return (

        <div
            className="w3-card w3-border w3-border-gray w3-round-large"
            style={{ marginTop: "2rem" }}>
            <header className="w3-container w3-opacity w3-light-gray" style={{padding: "1rem"}}>@{this.props.author}</header>
            <h1>Hello!! {this.state.name}</h1>
            <Popup id= {this.props.id}/>
            <div className="w3-container" style={{ padding: "2rem" }}>
                <h2 className="w3-xxlarge">
                    <span className="w3-opacity">{this.props.title}</span>
                    {this.props.isOwner &&
                    <button className="w3-right w3-button w3-red w3-large w3-hover-pale-red w3-round-large" onClick={() => deleteTweet(this.props.id)}>Delete                    
                    </button>}
                    <button className="w3-right w3-button w3-red w3-large w3-hover-pale-red w3-round-large" onClick={() => {
                        window.location = "/forecast"
                    }}>Get Forecast</button>
                    <button className="w3-right w3-button w3-red w3-large w3-hover-pale-red w3-round-large" onClick={() => {
                        document.getElementById("popup").style.display = "block"
                    }}>Popup</button>
                </h2>


                <div dangerouslySetInnerHTML={{__html: this.props.content}}/>
            </div>
        </div>
    );
}
}
export default TweetItem;