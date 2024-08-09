import { Component, OnInit, AfterViewInit } from '@angular/core';
import { faArrowTrendDown, faArrowTrendUp } from '@fortawesome/free-solid-svg-icons';
import { Chart, registerables } from 'chart.js';


@Component ({
    selector : 'app-dashboard',
    templateUrl : './dashboard.component.html',
    styleUrls : ['./dashboard.component.css']
})

export class DashboardComponent implements OnInit, AfterViewInit {
    public chart: any;
    public gainersList: any = [
		{
			"AAPL": 1.24982
		}
	];
    public gainersListKeys: string[] = [];
    public gainersListValues: number[] = [];
    public losersList: any = [
		{
			"MSFT": -0.29529
		},
		{
			"UL": -0.35878
		},
		{
			"WMT": -1.22526
		},
		{
			"NVDA": -5.1223
		}
	];
    public losersListKeys: string[] = [];
    public losersListValues: number[] = [];
    public faArrowTrendUp = faArrowTrendUp;
    public faArrowTrendDown = faArrowTrendDown;

    ngOnInit(): void {
        Chart.register(...registerables);

    }

    ngAfterViewInit(): void {
        this.renderChart();

        this.losersListKeys = [];
        this.losersListValues = [];

        for(var i=0; i<this.losersList.length; i++) {
            const key = Object.keys(this.losersList[i])[0];
            const value = this.losersList[i][key];
            
            this.losersListKeys.push(key);
            this.losersListValues.push(-1*value);
        }

        this.gainersListKeys = [];
        this.gainersListValues = [];
        
        for(var i=0; i<this.gainersList.length; i++) {
            const key = Object.keys(this.gainersList[i])[0];
            const value = this.gainersList[i][key];
            
            this.gainersListKeys.push(key);
            this.gainersListValues.push(value);
        }
    }

    renderChart(): void {
        // Sample data for the past 30 days
        const days = Array.from({ length: 30 }, (_, i) => `Day ${i + 1}`);
        const portfolioValues = Array.from({ length: 30 }, () => Math.floor(Math.random() * 1000));

        this.chart = new Chart('portfolioChart', {
            type: 'line',
            data: {
                labels: days,
                datasets: [
                    {
                        label: 'Portfolio Value',
                        data: portfolioValues,
                        borderColor: '#ecb176',
                        backgroundColor: '#ecb176',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                plugins: {
                    legend: {
                        labels: {
                        color: '#d4d7d7'  // Customize legend text color
                        }
                    },
                    tooltip: {
                        bodyColor: '#d4d7d7',  // Customize tooltip text color
                        titleColor: '#d4d7d7'
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            stepSize: 1,
                            display: false,
                            color: '#d4d7d7'  // Customize x-axis labels color
                        },
                        title: {
                            color: '#d4d7d7'  // Customize x-axis title color
                        }
                    },
                    y: {
                        ticks: {
                            stepSize: 100,
                            color: '#d4d7d7'  // Customize y-axis labels color
                        },
                        title: {
                            color: '#d4d7d7'  // Customize y-axis title color
                        }
                    }
                }
            }
        });
    }
}