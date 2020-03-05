import * as React from "react";
import { DatePicker } from 'antd';
import moment from "moment";
import axios from 'axios';
var api = require('../api/api');


const { RangePicker } = DatePicker;


export default class DetailedExpensesPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            fromDate: moment().startOf('month'),
            toDate: moment(),

        };
    }

    handleCalendarChange = (dates, datesString) => {
        this.setState({
           fromDate: dates[0],
           toDate: dates[1]
        });
        console.log(this.state);
    };

    getExpenseData = () => {

        axios.get('/api/expense_details')
            .then(res => {
                console.log(res);
            })
    };

    componentDidMount() {
        this.getExpenseData()
    }


    render() {
        return (
            <div>
                <RangePicker
                    onChange={(dates, datesString) => this.handleCalendarChange(dates, datesString)}
                    defaultValue={[this.state.fromDate, this.state.toDate]}
                    format={"DD/MM/YYYY"}
                />
                <div>
                    showing dates from {this.state.fromDate.toString()} to {this.state.toDate.toString()}
                </div>
            </div>
        );
    }
}