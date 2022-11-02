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
import {FaIconLibrary, FontAwesomeModule} from '@fortawesome/angular-fontawesome';
import {RouterModule} from '@angular/router';

import { faHouse, faBuildingShield, faBook, faCloudMoon} from '@fortawesome/free-solid-svg-icons';
import { PolicyComponent } from './modules/policy/policy.component';
import { ReadmeComponent } from './modules/readme/readme.component';

@NgModule({
    declarations: [
        AppComponent,
        ChartboxComponent,
        SidebarComponent,
        HeaderComponent,
        PolicyComponent,
        ReadmeComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        DashboardModule,
        FontAwesomeModule,
        RouterModule
    ],
    providers: [EnvServiceProvider],
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
