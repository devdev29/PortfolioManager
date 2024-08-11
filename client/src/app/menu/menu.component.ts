import { Component } from "@angular/core";
import { Router } from "@angular/router";
import { faChartLine, faUser, faRightFromBracket, faSackDollar } from "@fortawesome/free-solid-svg-icons";

@Component ({
    selector : 'app-menu',
    templateUrl : './menu.component.html',
    styleUrls : ['./menu.component.css']
})

export class MenuComponent {
    public clientName: string = "Kraus Usman";
    public activeButton: number = 1;

    faChartLine = faChartLine;
    faUser = faUser;
    faRightFromBracket = faRightFromBracket;
    faSackDollar = faSackDollar;

    constructor(private router: Router) {}

    ngOnInit() {
        // this.router.navigate(['/dashboard']);
        // this.activeButton = 1;
    }

    openDashboard() {
        this.activeButton = 1;
        console.log('Dashboard visible');
        // this.router.navigate(['/dashboard']);
    }

    openAsset() {
        this.activeButton = 2;
        console.log('Asset visible');
        // this.router.navigate(['/asset']);
    }

    openBuySell() {
        this.activeButton = 3;
        console.log('Profile visible');
    }

    openTransaction() {
        this.activeButton = 4;
        console.log('Transaction history visible');
    }
}