import * as React from "react";
import {DatePicker, PageHeader, Spin} from 'antd';
import moment from "moment";
import axios from 'axios';
import ExpenseDetailsTable from "./ExpenseDetailsTable";
import './DetailedExpensesPage.scss'


const {RangePicker} = DatePicker;


export default class DetailedExpensesPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            fromDate: moment().startOf('year'),
            toDate: moment(),
            expenses: null
        };
    }

    handleCalendarChange = (dates, datesString) => {
        this.setState({
            fromDate: dates[0],
            toDate: dates[1]
        }, () => {
            this.getExpenseData();
        });
    };

    setExpenses(expenses) {
        expenses.forEach((expense) => {
            expense.date = moment(expense.date.$date).format("DD/MM/YYYY");
            expense.key = expense._id
        });
        this.setState({
            expenses: expenses
        })
    }

    getExpenseData = () => {

        axios.get('/api/expense_details', {
            params: {
                fromDate: this.state.fromDate.format("DD-MM-YYYY"),
                toDate: this.state.toDate.format("DD-MM-YYYY")
            }
        })
            .then(res => {
                this.setExpenses(res.data);
            })
    };

    componentDidMount() {
        this.getExpenseData()
    }


    render() {
        let loadingOrComponent;
        if (this.state.expenses) {
            loadingOrComponent = <ExpenseDetailsTable expenses={this.state.expenses}/>
        }
        else {
            loadingOrComponent =  <Spin size="large" tip="Loading Expenses..." className="loading"/>
        }
        return (
            <div>
                <PageHeader
                    title="Detailed Expenses"
                    extra={
                        <RangePicker
                            onChange={(dates, datesString) => this.handleCalendarChange(dates, datesString)}
                            format={"DD/MM/YYYY"}
                            defaultValue={[this.state.fromDate, this.state.toDate]}
                        />
                    }
                />
                {loadingOrComponent}
            </div>
        );
    }
}