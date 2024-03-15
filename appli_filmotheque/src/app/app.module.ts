import { NgModule} from "@angular/core";
import { BrowserModule} from "@angular/platform-browser";
import { AppRoutingModule} from "./app-routing.module";
import { AppComponent} from "./app.component";

import { LoginComponent } from  './login/login.component';
import { SignupComponent } from  './signup/signup.component';
import { DashBoardComponent } from  './dashboard/dashboard.component' ;
import { ReactiveFormsModule} from "@angular/forms";
import { HttpClientModule} from "@angular/common/http";


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SignupComponent,
    DashBoardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule{ }
