import * as React from "react";
import {PageHeader, Spin} from 'antd';
import ExpenseRangePicker from "../ExpenseRangePicker";
import ExpenseSummeryTable from "./ExpenseSummeryTable";
import SummaryStatusTable from "./SummaryStatusTable";
import IncomeTable from "./IncomeTable";
import ExpensesTable from "./ExpensesTable";
import InvestmentsTable from "./InvestmentsTable";
import Loading from "../loading";


export default class SummaryPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            fromDate: null,
            toDate: null,
            expenses: null,
            months: []
        };
    }

    setDates = (fromDate, toDate) => {
        this.setState({
            fromDate: fromDate,
            toDate: toDate,
        });
    };


    render() {
        let loadingOrComponent;
        if (this.state.expenses) {
            loadingOrComponent = <ExpenseSummeryTable expenses={this.state.expenses} months={this.state.months}/>
        } else {
            loadingOrComponent = <Spin size="large" tip="Loading Expenses..." className="loading"/>
        }

        let ready = this.state.fromDate && this.state.toDate;

        return (
            <div>
                <PageHeader
                    title="Summery Expenses"
                    extra={
                        <ExpenseRangePicker handleDates={this.setDates}/>
                    }
                />
                {/*{ready ? <SummaryStatusTable fromDate={this.state.fromDate} toDate={this.state.toDate}/> : <Loading/>}*/}
                {/*{ready ? <IncomeTable fromDate={this.state.fromDate} toDate={this.state.toDate}/> : <Loading/>}*/}
                {ready ? <ExpensesTable fromDate={this.state.fromDate} toDate={this.state.toDate}/> : <Loading/>}
                {/*{ready ? <InvestmentsTable fromDate={this.state.fromDate} toDate={this.state.toDate}/> : <Loading/>}*/}
                {loadingOrComponent}
            </div>
        );
    }


}