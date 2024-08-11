import { HttpClient } from '@angular/common/http';
import { Component, Injectable } from '@angular/core';
import { faArrowTrendDown, faArrowTrendUp, faNewspaper } from '@fortawesome/free-solid-svg-icons';
import { Chart, registerables } from 'chart.js';
import { catchError, Observable, throwError } from 'rxjs';
import { AppComponent } from '../app.component';

@Component ({
    selector : 'app-dashboard',
    templateUrl : './dashboard.component.html',
    styleUrls : ['./dashboard.component.css']
})

@Injectable({
    providedIn: 'root'
})

export class DashboardComponent {
    public chart: any;

    public portfolioValuation: number = 0;
    public returnValue: number = 0;
    public inflow: number = 0;
    public outflow: number = 0;

    public days: string[] = [];
    public values: number[] = [];
    public mcapList: string[] = ['small', 'medium', 'large']
    public mcapValue: number[] = [0, 0, 0]
    public investmentList: string[] = [];
    public investmentValue: number[] = [];

    public gainersList: any = [];
    public gainersListKeys: string[] = [];
    public gainersListValues: number[] = [];
    public losersList: any = [];
    public losersListKeys: string[] = [];
    public losersListValues: number[] = [];
    public newsList: any = [];

    public faArrowTrendUp = faArrowTrendUp;
    public faArrowTrendDown = faArrowTrendDown;
    public faNewspaper = faNewspaper;

    public colorPalette: string[] = ["#370617","#6a040f","#9d0208","#d00000","#dc2f02","#e85d04","#f48c06","#faa307","#ffba08"];
    public totalInvestment: number = 0;

    constructor(private http: HttpClient, private app: AppComponent) { 
        Chart.register(...registerables);
    }

    errorHandler(error: {
        error: { message: string; };
        status: any; message: any;
    }) {
        let errorMessage = '';
        if (error.error instanceof ErrorEvent) {
            errorMessage = error.error.message;
        } 
        else {
            errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
        }
        return throwError(errorMessage);
    }

    getReturns(): Observable<any> {
        return this.http.get(this.app.domain + 'stocks/portfolio/returns').pipe(catchError(this.errorHandler));
    }

    getPortfolioValue(): Observable<any> {
        return this.http.get(this.app.domain + 'value/today').pipe(catchError(this.errorHandler));
    }

    getHistory(): Observable<any> {
        return this.http.get(this.app.domain + 'value/history').pipe(catchError(this.errorHandler));
    }

    getGainersLosers(): Observable<any> {
        return this.http.get(this.app.domain + 'stocks/portfolio/performance').pipe(catchError(this.errorHandler));
    }

    getStocks(): Observable<any> {
        return this.http.get(this.app.domain + 'stocks/portfolio/all').pipe(catchError(this.errorHandler));
    }

    getNewsArticles(): Observable<any> {
        return this.http.get('https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=42f3d82f9cdb45e987ba4bb6a8fcaa2f').pipe(catchError(this.errorHandler));
    }

    ngOnInit(): void {
        this.getPortfolioValue().subscribe(data => {
            console.log(data);
            this.portfolioValuation = data.value;
            this.inflow = data.inflow;
            this.outflow = -1*data.outflow;
        });

        this.getGainersLosers().subscribe(data => {
            this.gainersList = [...data.gainers].reverse();
            this.losersList = [...data.losers].reverse();
            console.log(this.gainersList);
            console.log(this.losersList);

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
        });

        this.getHistory().subscribe(data => {
            console.log(JSON.stringify(data));
            this.days = [];
            this.values = [];

            for(var i=0; i<data.length; i++) {
                this.days.push(data[i].day);
                let val: number = data[i].value;
                this.values.push(parseFloat((val / 1000).toFixed(3)));
            }
            this.renderPortfolioChart();
        });

        this.getStocks().subscribe(data => {
            console.log(JSON.stringify(data));
            this.mcapList = ['small', 'medium', 'large']
            this.mcapValue = [0, 0, 0]
            this.investmentList = [];
            this.investmentValue = [];
            for(var i=0; i<data.length; i++) {
                if(data[i].market_cap === 'large')
                    this.mcapValue[2]++;
                if(data[i].market_cap == 'medium')
                    this.mcapValue[1]++;
                if(data[i].market_cap == 'small')
                    this.mcapValue[0]++;
                this.investmentList.push(data[i].ticker);
                this.investmentValue.push(data[i].amount_invested);
                this.totalInvestment += data[i].amount_invested;
            }
            
            this.renderCompanyChart(commonOptions);
            this.renderMarketCapChart(commonOptions);
        });

        const commonOptions = {
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#d4d7d7',
                        boxWidth: 20
                    }
                },
                tooltip: {
                    bodyColor: '#d4d7d7',
                    titleColor: '#d4d7d7'
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                        color: '#d7d7d7ff'
                    },
                    ticks: {
                        stepSize: 1,
                        display: false,
                        color: '#d4d7d7'
                    },
                    title: {
                        color: '#d4d7d7'
                    }
                },
                y: {
                    grid: {
                        display: false,
                        color: '#d7d7d755'
                    },
                    ticks: {
                        display: false,
                        stepSize: 100,
                        color: '#d4d7d7'
                    },
                    title: {
                        color: '#d4d7d7'
                    }
                }
            },
            layout: {
                padding: {
                    right: 80,  // Reserve space for the legend
                    left: 0
                }
            }
        };

        this.days = ['Fri, 12 Jul 2024 00:00:00 GMT', 'Sat, 10 Aug 2024 00:00:00 GMT', 'Sun, 11 Aug 2024 00:00:00 GMT'];
        this.values = [243.994, 298.239, 299.076];
        this.renderPortfolioChart();

        this.getNewsArticles().subscribe(data => {
            console.log(data);
            this.newsList = data.articles.slice(0, 5);
        });

        this.getReturns().subscribe(data => {
            console.log(data);
            this.returnValue = data.returns;
        });
    }

    renderPortfolioChart(): void {
        const days = this.days;
        const portfolioValues = this.values;

        console.log(days);
        console.log(portfolioValues);

        this.chart = new Chart('portfolioChart', {
            type: 'line',
            data: {
                labels: days,
                datasets: [
                    {
                        label: 'Portfolio Value (in thousand dollars)',
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
                        titleColor: '#d4d7d7',
                        callbacks: {
                            label: function(tooltipItem: any) {
                                let label = tooltipItem.label || '';
                                if (label) {
                                    label += ': $';
                                }
                                label += tooltipItem.raw + 'k';
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                            color: '#d7d7d7ff'
                        },
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
                        grid: {
                            display: true,
                            color: '#d7d7d755'
                        },
                        ticks: {
                            stepSize: 10,
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

    renderCompanyChart(commonOptions: any): void {
        this.chart = new Chart('companyChart', {
            type: 'doughnut',
            data: {
                labels: this.investmentList,
                datasets: [{
                    label: 'Investment Distribution',
                    data: this.investmentValue,
                    backgroundColor: [...this.colorPalette].reverse().slice(0, this.investmentList.length),
                    hoverOffset: 5, // Grow the segment on hover
                    borderColor: '#222222',
                    borderWidth: 4
                }]
            },
            options: commonOptions
        });
    }

    renderMarketCapChart(commonOptions: any): void {
        this.chart = new Chart('marketCapChart', {
            type: 'doughnut',
            data: {
                labels: this.mcapList,
                datasets: [{
                    label: 'Market Cap Distribution',
                    data: this.mcapValue,
                    backgroundColor: ['#e85d04', '#6a040f', '#ffba08'],
                    hoverOffset: 5, // Grow the segment on hover
                    borderColor: '#222222',
                    borderWidth: 4
                }]
            },
            options: commonOptions
        });
    }
}