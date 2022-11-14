import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChartboxComponent } from './chartbox.component';

describe('ChartboxComponent', () => {
  let component: ChartboxComponent;
  let fixture: ComponentFixture<ChartboxComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChartboxComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChartboxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
