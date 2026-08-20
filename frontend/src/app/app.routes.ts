import { Routes } from '@angular/router';

import { Landing } from './features/landing/landing';
import { Login } from './features/auth/login/login';
import { Register } from './features/auth/register/register';
import { GuestQuiz } from './features/guest/guest-quiz/guest-quiz';

export const routes: Routes = [
  {
    path: '',
    component: Landing,
  },
  {
    path: 'login',
    component: Login,
  },
  {
    path: 'register',
    component: Register,
  },
  {
    path: 'guest/quiz',
    component: GuestQuiz,
  },
];

