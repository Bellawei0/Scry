import React from "react";
import DataItem from "./DataItem";
import Axios from "axios";
import AddProduct from "./AddProduct";
import Logout from "./Logout";
import Popup from "./Popup";

class MainPage extends React.Component {
  state = { products: [], currentUser: { username: "" } };
  componentDidMount() {
    Axios.get("/api/products").then((res) => {
      this.setState({ products: res.data.reverse() });
    });
    setTimeout(() => {
      Axios.get("/api/getcurrentuser", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }).then((res) => {
        this.setState({ currentUser: res.data });
      });
    }, 500);
  }

  render() {
    return (
      <React.Fragment>
        <div className="w3-container w3-light-grey">
          <div
            className="w3-container w3-jumbo"
            style={{ margin: "3rem", paddingLeft: "1rem" }}
          >
            <h1>Products</h1>
          </div>
          <div
            className="w3-container w3-jumbo"
            style={{ margin: "3rem", paddingLeft: "1rem" }}
          >
            <button
              className="w3-button w3-blue w3-large"
              onClick={() => {
                document.getElementById("addProduct").style.display = "block";
              }}
            >
              Add Product
            </button>
            {/* <button
            className="w3-right w3-button w3-red w3-large w3-hover-pale-red w3-round-large"
            onClick={() => {
              window.location = "/logout";
            }}
          >
            Sign Out
          </button> */}
          </div>
          <AddProduct />
          <div className="w3-container">
            {this.state.products.length === 0 ? (
              <p
                className="w3-xlarge w3-opacity"
                style={{ marginLeft: "2rem" }}
              >
                No Products, Create one
              </p>
            ) : (
              this.state.products.map((item, index) => {
                return (
                  <DataItem
                    id={item.id}
                    title={item.ProductName}
                    content={item.Description}
                    author={item.user.username}
                    isOwner={
                      this.state.currentUser.username === item.user.username
                    }
                    key={index}
                  />
                );
              })
            )}
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default MainPage;
