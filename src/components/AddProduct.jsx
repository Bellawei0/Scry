import React from "react";
import {Editor} from "@tinymce/tinymce-react/lib/cjs/main/ts";
import Axios from "axios";
import Alert from "./Alert";

class AddProduct extends React.Component 
{
    state = 
    {

        content: "<p>I have to edit this!</p>", 
        titleErr: "", 
        contentErr: "", 
        formErr: ""
    }

    handleEditorChange = (content, editor) => 
    {
        console.log(content)
        this.setState({content})
    }


    submitForm = (e) => 
    {
        e.preventDefault()

        if (this.state.content.length === 0) 
        {
            this.setState({contentErr: "Add a Description"})
            return;
        }
        
        if (document.getElementById("title").value.length === 0) 
        {
            this.setState({titleErr: "Add a Product Name"})
            return;
        }
        
        var formData = new FormData();
        var imagefile = document.querySelector('#file');
        formData.append("image", imagefile.files[0]);
        formData.append("title", document.getElementById("title").value);
        formData.append("content", this.state.content);
        Axios.post('/api/addproduct', formData, 
        {
            headers: 
            {
                Authorization: "Bearer " + localStorage.getItem("token"),
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(res => 
        {
            if (res.data.success) 
            {
                window.location.reload()
            } 
            else 
            {
                this.setState({formErr: res.data.error })
            }
        })
    }

    render() 
    {
        return (<div className="w3-modal w3-animate-opacity" id="addProduct">
            <div className="w3-modal-content w3-card">
                <header className="w3-container w3-blue">
                <span className="w3-button w3-display-topright w3-hover-none w3-hover-text-white" onClick={() => {
                    document.getElementById("addProduct").style.display = "none"
                }}>X</span>
                    <h2>Add Product</h2>
                </header>
                <form className="w3-container" id = "myform" onSubmit={this.submitForm}>
                <input type="file" id="file" name="file"/>
                    {this.state.formErr.length > 0 && <Alert message={this.state.formErr}/>}
                    <div className="w3-section">
                        <p>
                            <label htmlFor="title">Product Name</label>
                            <input type="text" id="title" className="w3-input w3-border w3-margin-bottom"/>
                            <small className="w3-text-gray">{this.state.titleErr}</small>
                        </p>
                        <p>
                        <Editor
                            initialValue="<p>Enter a product description</p>"
                            apiKey='4i9uvjc8q9bxptbwdvoo0w1gx2b2ich8v32d2kskukqnxiqh'
                            init={{
                                height: 300,
                                menubar: false,
                                statusbar: false,
                                toolbar_mode: "sliding",
                                plugins: [
                                    'advlist autolink lists link image imagetools media emoticons preview anchor',
                                    'searchreplace visualblocks code fullscreen',
                                    'insertdatetime media table paste code help wordcount'
                                ],
                                toolbar:
                                    'undo redo | formatselect | bold italic underline strikethrough | image anchor media | \
                                    alignleft aligncenter alignright alignjustify | \
                                    outdent indent | bulllist numlist | fullscreen preview | emoticons help',
                                contextmenu: "bold italic underline indent outdent help"
                            }}
                            onEditorChange={this.handleEditorChange}
                        />
                            <small className="w3-text-gray">{this.state.contentErr}</small>
                        </p>
                        <p>
                            <button type="submit" className="w3-button w3-blue">Post</button>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    )}
}

export default AddProduct