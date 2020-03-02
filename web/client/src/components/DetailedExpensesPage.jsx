import * as React from "react";
import { DatePicker } from 'antd';
import moment from "moment";

const { RangePicker } = DatePicker;



export default class DetailedExpensesPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            fromDate: moment(),
            toDate: new Date(),

        };
    }

    handleCalendarChange = (dates, datesString) => {
        console.log(dates);
        console.log(datesString);
    };


    render() {
        return (
            <div>
                <RangePicker onChange={(dates, datesString) => this.handleCalendarChange(dates, datesString)}/>
            </div>
        );
    }
}