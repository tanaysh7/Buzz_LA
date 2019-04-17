import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { BuzzLandingComponent } from './buzz-landing/buzz-landing.component';

@NgModule({
  declarations: [
    AppComponent,
    BuzzLandingComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
