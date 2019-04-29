import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BuzzLandingComponent } from './buzz-landing.component';

describe('BuzzLandingComponent', () => {
  let component: BuzzLandingComponent;
  let fixture: ComponentFixture<BuzzLandingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BuzzLandingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BuzzLandingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
