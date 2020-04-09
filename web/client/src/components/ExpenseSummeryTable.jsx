import * as React from "react";
import {Table} from "antd";
import "./ExpenseDetailsTable.scss"


export default class ExpenseSummeryTable extends React.Component {

    constructor(props) {
        super(props);
        this.tableColumns = [
            {
                title: 'Category Type',
                dataIndex: 'categoryType',
            },
            {
                title: 'Category',
                dataIndex: 'category',
            },
            {
                title: 'Average',
                dataIndex: 'average',
            }];
    }


    render() {
        return (
            <div>
                <Table dataSource={this.props.expenses} columns={this.tableColumns}
                       rowClassName={(record, index) => record.amount > 0 ? "credit-row" : 'debit-row'}
                       pagination={{ defaultPageSize: 50}}
                       scroll={{ y: 550 }}
                       size="small"
                />
            </div>
        );
    }
}