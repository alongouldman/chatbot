import * as React from "react";
import ExpenseSummeryTable from "./ExpenseSummeryTable";


export default class SummaryStatusTable extends React.Component {

    constructor(props) {
        super(props);
        this.categoryTypes = []
    }


    render() {
        return (
            <div>
                {/*<ExpenseSummeryTable fromDate={this.props.fromDate} toDate={this.props.toDate} categoryTypes={this.categoryTypes}/>*/}
                SummaryStatusTable
            </div>
        );
    }
}