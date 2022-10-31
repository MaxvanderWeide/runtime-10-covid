import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {EnvServiceProvider} from "./services/env.service.provider";
import {HttpClientModule} from "@angular/common/http";
import { ChartboxComponent } from './components/chartbox/chartbox.component';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import {DashboardModule} from "./modules/dashboard/dashboard.module";
import {HeaderComponent} from "./components/header/header.component";

@NgModule({
    declarations: [
        AppComponent,
        ChartboxComponent,
        SidebarComponent,
        HeaderComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        DashboardModule
    ],
    providers: [EnvServiceProvider],
    bootstrap: [AppComponent]
})
export class AppModule {

}
