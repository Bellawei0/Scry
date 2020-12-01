import React from "react";

class Derp extends React.Component
{

    submitForm = (e) => 
    {
        e.preventDefault()
        
        
        if (document.getElementById("derp").value.length === 0) 
        {
            this.setState({titleErr: "Add a title!"})
            return;
        }
        const params = new URLSearchParams(window.location.search)
        const foo = params.get('id')
        var w = document.getElementById("derp").value
        window.location = "/forecast?id=" + foo +"&length=" + w
    }

    render() {
    return (
        <div className="w3-container w3-center" style={{margin: "3rem"}}>
             <form className="w3-container" onSubmit={this.submitForm}>
                    <div className="w3-section">
                            <label htmlFor="yoyo">How many periods do you want to forecast?</label>
                            <input type="text" id="derp" className="w3-input w3-border w3-margin-bottom"/>
                        <p>
                            <button type="submit" className="w3-button w3-blue">Get Forecast</button>
                        </p>
                    </div>
              </form>
                      	<button type="button" className="w3-button w3-blue" onClick={() => window.location = "/"}>&laquo; Back</button>

        </div>

    )
}
}
export default Derp;