import * as React from "react";
import {Table} from "antd";
import moment from "moment";
import "./ExpenseDetailsTable.scss"


export default class ExpenseDetailsTable extends React.Component {

    constructor(props) {
        super(props);
        console.log(this.props.expenses);

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
                sorter: (a, b) => a.category.localeCompare(b.category),
                filters: filters,
                onFilter: (value, record) => record.category === value
            },
            {
                title: 'Date',
                dataIndex: 'date',
                sorter: (a, b) => moment(a.date, "DD/MM/YYYY").unix() - moment(b.date, "DD/MM/YYYY").unix()
            },
            {
                title: 'Description',
                dataIndex: 'description',
                sorter: (a, b) => {
                    if (!('description' in a)) {
                        return 1;
                    }
                    else if (!('description' in b)) {
                        return -1;
                    }
                    else {
                        return a.description.localeCompare(b.description);
                    }
                }
            },
        ];
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