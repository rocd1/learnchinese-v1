import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GuestQuiz } from './guest-quiz';

describe('GuestQuiz', () => {
  let component: GuestQuiz;
  let fixture: ComponentFixture<GuestQuiz>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GuestQuiz],
    }).compileComponents();

    fixture = TestBed.createComponent(GuestQuiz);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
