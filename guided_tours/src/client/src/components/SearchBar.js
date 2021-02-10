import React, { Component } from "react";
import Autosuggest from "react-autosuggest";
import { withRouter } from "react-router";
import "../styles/SearchBar.css";

// This code is based on the example from the react-autosuggest repo:
// https://github.com/moroshko/react-autosuggest


class SearchBar extends Component {
  constructor() {
    super();

    this.state = {
      value: "",
      suggestions: [],
    };

    this.onKeyDown = this.onKeyDown.bind(this);
  }

  renderSuggestion = suggestion => (
    <div>
      {suggestion.title}
    </div>
  );

  getSuggestionValue = suggestion => {
    return suggestion.title
  };

  onChange = (event, { newValue }) => {
    this.setState({
      value: newValue
    });
  };

  // Autosuggest will call this function every time you need to update suggestions.
  // You already implemented this logic above, so just use it.
  onSuggestionsFetchRequested = ({ value }) => {
    const inputValue = value.trim().toLowerCase();
    const inputLength = inputValue.length;
    this.getSuggestions(inputValue, inputLength);
  }

  getSuggestions = (inputValue, inputLength) => {
    let suggestions = inputLength === 0 ? [] : this.props.tours.filter(tour =>
      tour.title.toLowerCase().slice(0, inputLength) === inputValue
    );

    this.setState({
      suggestions: suggestions
    });
  }


  onKeyDown = event => {
    if (event.key === "Enter") {
      this.handleRedirectToTour();
    }
  }

  handleRedirectToTour = () => {
    let tour_id = null;
    let tour_title = this.state.value;

    this.props.tours.forEach(function(tour) {
      if (tour.title === tour_title) {
        tour_id = tour.tour_id;
      }
    });

    if (tour_id === null) {
      alert("Error lookuping up tour");
      return null;
    }
    this.props.history.push({
      pathname: `/tours/${tour_id}`
   })
  }

  onSuggestionsClearRequested = () => {
    this.setState({
      suggestions: []
    });
  };

  render = () => {
    const { value, suggestions } = this.state;

    const inputProps = {
      placeholder: "Search Local Tours",
      value,
      onChange: this.onChange,
      onKeyDown: this.onKeyDown
    };

    return (
      <Autosuggest
        id="searchSuggestionId"
        class="searchSuggestion"
        suggestions={suggestions}
        onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
        onSuggestionsClearRequested={this.onSuggestionsClearRequested}
        getSuggestionValue={this.getSuggestionValue}
        renderSuggestion={this.renderSuggestion}
        inputProps={inputProps}
      />
    );
  }
}

export default withRouter(SearchBar);
