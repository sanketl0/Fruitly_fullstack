import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UserComponent } from './components/user/user.component';
import { HomepageComponent } from './components/homepage/homepage.component';
import { authGuard } from './auth.guard';

const routes: Routes = [
  { path: 'register', component: UserComponent },
  { path: 'login', component: UserComponent },
  { path: 'home', component: HomepageComponent,canActivate: [authGuard] },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
