import * as React from "react";
import {DatePicker} from 'antd';
import moment from "moment";
const {RangePicker} = DatePicker;


export default class ExpenseRangePicker extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            fromDate: moment().startOf('year'),
            toDate: moment(),
        };
    }

    handleCalendarChange = (dates, datesString) => {
        this.setState({
            fromDate: dates[0],
            toDate: dates[1]
        }, () => {
            this.props.handleDates(this.state.fromDate, this.state.toDate);
        });
    };

    componentDidMount() {
        this.props.handleDates(this.state.fromDate, this.state.toDate);
    }

    render() {
        return (
            <div>
                <RangePicker
                    onChange={(dates, datesString) => this.handleCalendarChange(dates, datesString)}
                    format={"DD/MM/YYYY"}
                    defaultValue={[this.state.fromDate, this.state.toDate]}
                />
            </div>
        );
    }
}