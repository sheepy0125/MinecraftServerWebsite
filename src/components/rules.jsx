import {Component} from "react";
import {get} from "axios";

export default class Rules extends Component {
	state = {
		rulesList: null
	};

	// Get rules
	getRules = () => {
		get("get_rules")
			.then((rulesResult) => {
				if (rulesResult.data.worked) this.setState({rulesList: rulesResult.data.rules});
				else this.setState({rulesList: null});
			})
			.catch((result) => {
				this.setState({rulesList: null});
			});
	};

	// Display rules
	displayRules = () => {
		let rulesDivs = [];

		this.state.rulesList.forEach((rule) => {
			rulesDivs.push(
				<div className="bg-gray-200 border-2 border-gray-300 m-1 p-2 text-center rounded-lg" key={rulesDivs.length}>
					{rule}
				</div>
			);
		});

		return rulesDivs;
	};

	componentDidMount = () => {
		this.getRules();
	};

	render = () => {
		return (
			<div className="bg-opacity-50 hover:bg-opacity-75 bg-gray-50 p-4">
				<p className="font-semibold">Rules</p>
				<div>{this.state.rulesList !== null ? this.displayRules() : "No information."}</div>
			</div>
		);
	};
}
