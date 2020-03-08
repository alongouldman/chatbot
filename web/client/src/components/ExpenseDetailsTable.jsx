import * as React from "react";
import {Table} from "antd";
import moment from "moment";
import "./ExpenseDetailsTable.scss"


export default class ExpenseDetailsTable extends React.Component {

    constructor(props) {
        super(props);
        let allCategories = new Set();
        this.props.expenses.forEach((expense) => {
            allCategories.add(expense.category);
        });
        let filters = [];
        allCategories.forEach((category) => {
            filters.push({
                text: category.charAt(0).toUpperCase() + category.slice(1),
                value: category
            });
        });

        this.tableColumns = [
            {
                title: 'Amount',
                dataIndex: 'amount',
                key: 'amount',
                sorter: (a, b) => a.amount - b.amount,
                className: "amount",
                filters: [{
                    text: 'Credit',
                    value: 'credit'
                },
                    {
                        text: 'Debit',
                        value: 'debit'
                    }],
                onFilter: (value, record) => {
                    if (value === 'credit') {
                        return record.amount > 0
                    }
                    else {
                        return record.amount <= 0
                    }
                }

            },
            {
                title: 'Category',
                dataIndex: 'category',
                key: 'category',
                sorter: (a, b) => a.category.localeCompare(b.category),
                filters: filters,
                onFilter: (value, record) => record.category === value
            },
            {
                title: 'Date',
                dataIndex: 'date',
                key: 'date',
                sorter: (a, b) => moment(a.date, "DD/MM/YYYY").unix() - moment(b.date, "DD/MM/YYYY").unix()
            },
        ];
    }


    render() {
        return (
            <div>
                <Table dataSource={this.props.expenses} columns={this.tableColumns}
                       rowClassName={(record, index) => record.amount > 0 ? "credit-row" : 'debit-row'}
                />;
            </div>
        );
    }
}