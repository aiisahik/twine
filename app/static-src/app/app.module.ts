import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RequestOptions, HttpModule } from '@angular/http';
import { AUTH_PROVIDERS } from 'angular2-jwt';
import { MaterialModule } from '@angular/material';

import { RouterModule, Routes } from '@angular/router';
import { AuthRequestOptions } from './auth/auth.service';
import { AuthService } from './auth/auth.service';
// import { AuthModule } from './auth/auth.module';

import { AppComponent } from './app.component';
import { NotFoundComponent }    from './not-found/not-found.component';
import { Profile } from './_models/profile';
import { LoginComponent } from './login/login.component';

const appRoutes: Routes = [
  {
    path: 'battle',
    loadChildren: 'app/battle/battle.module#BattleModule',
  },
  // { path: '',   component: AppComponent },
  { path: 'login', component: LoginComponent },
  { path: '**', component: NotFoundComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    NotFoundComponent,
    LoginComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MaterialModule,
    FormsModule,
    HttpModule,
    RouterModule.forRoot(
      appRoutes,
    )
  ],
  exports: [
    RouterModule
  ],
  providers: [
    // { provide: RequestOptions, 
    //   useClass: DefaultRequestOptions, 
        // useExisting: forwardRef(() => AlexComponent)
    //   deps: [AuthService]
    // },
    // { provide: RequestOptions, useClass: DefaultRequestOptions },
    AuthService,
    AuthRequestOptions,
    // {
    //   provide: AuthHttp,
    //   useFactory: authHttpServiceFactory,
    // }
    // requestOptionsProvider,
    // AuthGuard, 
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
