import React from "react";
import {Editor} from "@tinymce/tinymce-react/lib/cjs/main/ts";
import Axios from "axios";
import Alert from "./Alert";

class Popup extends React.Component {
    constructor(props) {
    super(props);
    }
    state = 
    {
        content: "<p>I have to edit this!</p>", titleErr: "", contentErr: "", formErr: ""
    }

    handleEditorChange = (content, editor) => 
    {
        console.log(content)
        this.setState({content})
    }

    submitForm = (e) => 
    {
        e.preventDefault()
        
        
        if (document.getElementById("derp").value.length === 0) 
        {
            this.setState({titleErr: "Add a title!"})
            return;
        }
        
        Axios.post("/api/makeRequest", 
        {
            title: this.props.id,
            content: document.getElementById("derp").value
        }, 
        {
            headers: 
            {
                Authorization: "Bearer " + localStorage.getItem("token")
            }
        }).then(res => 
        {
            if (res.data.success) 
            {
                window.location = "/forecast"
            } 
            else 
            {
                this.setState({formErr: res.data.error })
            }
        })
    }

    render() {
        return (<div className="w3-modal w3-animate-opacity" id="popup">
            <div className="w3-modal-content w3-card">
                <header className="w3-container w3-blue">
                <span className="w3-button w3-display-topright w3-hover-none w3-hover-text-white" onClick={() => {
                    document.getElementById("popup").style.display = "none"
                }}>X</span>
                    <h2>{this.props.id}</h2>
                </header>
                <form className="w3-container" onSubmit={this.submitForm}>
                    {this.state.formErr.length > 0 && <Alert message={this.state.formErr}/>}
                    <div className="w3-section">
                            <label htmlFor="yoyo">How many periods do you want to forecast?</label>
                            <input type="text" id="derp" className="w3-input w3-border w3-margin-bottom"/>
                            <small className="w3-text-gray">{this.state.titleErr}</small>
                        <p>
                            <button type="submit" className="w3-button w3-blue">{this.props.id}</button>
                        </p>
                    </div>
                </form>
            </div>
        </div>)
    }
}

export default Popup