import React, { useState } from "react";
import { connect } from "react-redux";
import agent from "../../agent";
import { SEARCH_ITEMS } from "../../constants/actionTypes";

const mapDispatchToProps = (dispatch) => ({
  onSearch: (title, pager, payload) =>
    dispatch({ type: SEARCH_ITEMS, title, pager, payload }),
});

const SearchBar = (props) => {
  const [value, setValue] = useState("");

  const handleChange = (event) => {
    const title = event.target.value;
    setValue(title);
    if (title.length > 2) {
      console.log(`search ${title}`);
      const pager = agent.Items.byTitle;
      const payload = agent.Items.byTitle(title, 0);
      props.onSearch(title, pager, payload);
    }
  };

  return (
    <form>
      <input
        type="text"
        placeholder="What is it that you truly desire?"
        value={value}
        onChange={handleChange}
      />
      <span>&#x1F50D;</span>
    </form>
  );
};

export default connect(null, mapDispatchToProps)(SearchBar);
