import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {EnvServiceProvider} from "./services/env.service.provider";
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import { ChartboxComponent } from './components/chartbox/chartbox.component';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import {DashboardModule} from "./modules/dashboard/dashboard.module";
import {HeaderComponent} from "./components/header/header.component";
import {FaIconLibrary, FontAwesomeModule} from '@fortawesome/angular-fontawesome';
import {RouterModule} from '@angular/router';

import { faHouse, faBuildingShield, faBook, faCloudMoon} from '@fortawesome/free-solid-svg-icons';
import { PolicyComponent } from './modules/policy/policy.component';
import { ReadmeComponent } from './modules/readme/readme.component';
import {DashboardComponent} from "./modules/dashboard/dashboard.component";
import {NgxChartsModule} from "@swimlane/ngx-charts";
import {TokenInterceptor} from "./auth/token.interceptor";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

@NgModule({
    declarations: [
        AppComponent,
        ChartboxComponent,
        SidebarComponent,
        HeaderComponent,
        DashboardComponent,
        PolicyComponent,
        ReadmeComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        NgxChartsModule,
        BrowserAnimationsModule,
        FontAwesomeModule,
        RouterModule,
    ],
    providers: [
        {
            provide: HTTP_INTERCEPTORS,
            useClass: TokenInterceptor,
            multi: true
        },
        EnvServiceProvider],
    exports: [
        ChartboxComponent
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
    constructor(library: FaIconLibrary) {
        library.addIcons(faHouse, faBuildingShield, faBook, faCloudMoon);
    }
}
