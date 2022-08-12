import SearchBar from "./SearchBar";
import React, { useState } from "react";
import logo from "../../imgs/logo.png";

const Banner = () => {
  const [searchVisible, setSearchVisible] = useState(false);

  return (
    <div className="banner text-white">
      <div className="container p-4 text-center">
        <img src={logo} alt="banner" />
        <div
          style={{
            height: "50px",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <span>A place to&nbsp;</span>
          <span
            id="get-part"
            onClick={() => setSearchVisible((prevValue) => !prevValue)}
          >
            get
          </span>
          {searchVisible ? <SearchBar /> : null}
          <span>the cool stuff.</span>
        </div>
      </div>
    </div>
  );
};

export default Banner;
