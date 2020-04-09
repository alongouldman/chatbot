import * as React from "react";
import {PageHeader, Spin} from 'antd';
import ExpenseDetailsTable from "./ExpenseDetailsTable";
import './DetailedExpensesPage.scss'
import ExpenseRangePicker from "./ExpenseRangePicker";
import axios from "axios";
import moment from "moment";


export default class DetailedExpensesPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expenses: null
        };
    }

    getExpenseData = (fromDate, toDate) => {
        axios.get('/api/expense_details', {
            params: {
                fromDate: fromDate.format("DD-MM-YYYY"),
                toDate: toDate.format("DD-MM-YYYY")
            }
        })
            .then((res) => {
                this.setExpenses(res.data);
            })
    };

    setExpenses = (expenses) => {
        expenses.forEach((expense) => {
            expense.date = moment(expense.date.$date).format("DD/MM/YYYY");
            expense.key = expense._id
        });
        this.setState({
                expenses: expenses
            }
        )
    };

    render() {
        let loadingOrComponent;
        if (this.state.expenses) {
            loadingOrComponent = <ExpenseDetailsTable expenses={this.state.expenses}/>
        } else {
            loadingOrComponent = <Spin size="large" tip="Loading Expenses..." className="loading"/>
        }
        return (
            <div>
                <PageHeader
                    title="Detailed Expenses"
                    extra={
                        <ExpenseRangePicker handleDates={this.getExpenseData}/>
                    }
                />
                {loadingOrComponent}
            </div>
        );
    }
}