import * as React from "react";
import ExpenseSummeryTable from "./ExpenseSummeryTable";
import {CategoryTypes} from "../../consts.jsx";

export default class ExpensesTable extends React.Component {

    constructor(props) {
        super(props);
        this.categoryTypes = [
            CategoryTypes.VITAL_AND_REOCCURING,
            CategoryTypes.VITAL_AND_CHANGES,
            CategoryTypes.UNNECESSARY_AND_REOCCURING,
            CategoryTypes.UNNECESSARY_AND_CHANGES,
            CategoryTypes.STUDY,
            CategoryTypes.UNKNOWN
        ]
    }


    render() {
        return (
            <div>
                <ExpenseSummeryTable fromDate={this.props.fromDate} toDate={this.props.toDate} categoryTypes={this.categoryTypes}/>
            </div>
        );
    }
}