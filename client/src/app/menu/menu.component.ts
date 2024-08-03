import { Component } from "@angular/core";
import { faChartLine, faUser, faRightFromBracket, faSackDollar } from "@fortawesome/free-solid-svg-icons";

@Component ({
    selector : 'app-menu',
    templateUrl : './menu.component.html',
    styleUrls : ['./menu.component.css']
})

export class MenuComponent {
    public clientName : string = "Kraus Usman";
    public activeButton : number = 1;
    faChartLine = faChartLine;
    faUser = faUser;
    faRightFromBracket = faRightFromBracket;
    faSackDollar = faSackDollar;

    openDashboard() {
        this.activeButton = 1;
        console.log('Dashboard visible');
    }
    openAsset() {
        this.activeButton = 2;
        console.log('Asset visible');
    }
    openProfile() {
        this.activeButton = 3;
        console.log('Profile visible');
    }
    openLogin() {
        this.activeButton = 4;
        console.log('Login visible');
    }

    onButtonGroupClick($event: MouseEvent) {
        
    }
}