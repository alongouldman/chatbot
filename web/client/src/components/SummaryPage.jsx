import * as React from "react";
import {PageHeader, Spin} from 'antd';
import ExpenseRangePicker from "./ExpenseRangePicker";
import ExpenseSummeryTable from "./ExpenseSummeryTable";
import axios from "axios";


export default class SummaryPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expenses: null,
            categories: null
        };
        // TODO: use promise for the categories, and get it when the component is mounting
    }

    getData = (fromDate, toDate) => {
        axios.get('/api/expense_summery', {
            params: {
                fromDate: fromDate.format("DD-MM-YYYY"),
                toDate: toDate.format("DD-MM-YYYY")
            }
        })
            .then(res => {
                this.populateData(res.data);
            })
    };

    populateData = (expenseData) => {
        console.log(expenseData);
    };


    render() {
        let loadingOrComponent;
        if (this.state.expenses) {
            loadingOrComponent = <ExpenseSummeryTable expenses={this.state.expenses}/>
        } else {
            loadingOrComponent = <Spin size="large" tip="Loading Expenses..." className="loading"/>
        }
        return (
            <div>
                <PageHeader
                    title="Summery Expenses"
                    extra={
                        <ExpenseRangePicker handleDates={this.getData}/>
                    }
                />
                {loadingOrComponent}
            </div>
        );
    }


}