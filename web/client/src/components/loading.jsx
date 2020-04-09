import * as React from "react";
import {Spin} from 'antd';


export default class Loading extends React.Component {

    render() {
        return (
            <div>
                <Spin size="large" tip="Loading Expenses..." className="loading"/>
            </div>
        );
    }
}