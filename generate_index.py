# -*- coding: utf-8 -*-
import os

html_code = r'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Superpersonalizado — Corte Láser y Arte en Madera 3D</title>
  <meta name="description" content="Figuras, cuadros multicapa y piezas personalizadas cortadas en madera de alta precisión con tecnología láser y acabado artesanal.">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Three.js Import Map -->
  <script type="importmap">
  {
    "imports": {
      "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.min.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
    }
  }
  </script>

  <style>
    :root {
      --ink: #1c1815;
      --cream: #f4ede4;
      --dark: #161311;
      --wood-warm: #8b5742;
      --flav: #8b5742;
      --rv: transparent;
      --wa-green: #25D366;
      --wa-hover: #1fb857;
      --ease: cubic-bezier(.22, .8, .24, 1);
      --u: min(100vw / 1440, 100vh / 900);
      --w: calc(100vw / 1440);
      --n: min(100vw / 1440, 1px);
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--cream);
      color: var(--ink);
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }

    body.locked {
      overflow: hidden;
    }

    body.dragging {
      cursor: grabbing !important;
      user-select: none;
    }

    .disp {
      font-family: 'Archivo Black', sans-serif;
      text-transform: uppercase;
      letter-spacing: -0.01em;
      line-height: 0.92;
    }

    .mono {
      font-family: 'DM Mono', monospace;
    }

    /* Canvas WebGL Layer */
    #gl {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      z-index: 2;
      pointer-events: none;
    }

    /* Intro Overlay */
    #intro {
      position: fixed;
      inset: 0;
      z-index: 100;
      background: #7a4835;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: opacity 0.8s var(--ease), visibility 0.8s;
      overflow: hidden;
    }

    #intro.hidden {
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }

    .intro-rings {
      position: absolute;
      width: 120vw;
      height: 120vw;
      border-radius: 50%;
      background: repeating-radial-gradient(circle, rgba(255,255,255,0.06) 0, rgba(255,255,255,0.01) 30px, rgba(255,255,255,0.06) 60px);
      animation: rotateRing 40s linear infinite;
    }

    @keyframes rotateRing {
      to { transform: rotate(360deg); }
    }

    .intro-stamp {
      position: relative;
      z-index: 2;
      text-align: center;
      color: #fff;
      transform: scale(0.9);
      animation: stampPop 1s var(--ease) forwards;
    }

    @keyframes stampPop {
      0% { opacity: 0; transform: scale(0.7) translateY(20px); }
      70% { opacity: 1; transform: scale(1.03) translateY(-2px); }
      100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    .intro-logo-box {
      width: 110px;
      height: 110px;
      margin: 0 auto 24px;
      background: rgba(255,255,255,0.12);
      border: 2px solid rgba(255,255,255,0.3);
      border-radius: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(8px);
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }

    .intro-logo-box svg {
      width: 64px;
      height: 64px;
      fill: #fff;
    }

    .intro-title {
      font-size: clamp(32px, 5vw, 68px);
      font-family: 'Archivo Black', sans-serif;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
      text-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }

    .intro-sub {
      font-family: 'DM Mono', monospace;
      font-size: 13px;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      opacity: 0.85;
    }

    .skip-pill {
      position: absolute;
      top: 32px;
      right: 36px;
      z-index: 3;
      height: 38px;
      padding: 0 22px;
      border-radius: 99px;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.4);
      color: var(--ink);
      font-family: 'DM Mono', monospace;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.15);
      transition: transform 0.2s, background 0.2s;
    }

    .skip-pill:hover {
      transform: scale(1.05);
      background: #fff;
    }

    /* Fixed Navigation with zero-collision flexbox */
    #nav {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 82px;
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 max(24px, 3.2vw);
      gap: 16px;
      background: linear-gradient(180deg, rgba(18, 14, 11, 0.72) 0%, rgba(18, 14, 11, 0.25) 75%, transparent 100%);
      color: #fff;
      transition: transform 0.4s var(--ease), background 0.3s ease;
    }

    #nav.light {
      background: linear-gradient(180deg, rgba(244, 237, 228, 0.95) 0%, rgba(244, 237, 228, 0.7) 75%, transparent 100%);
      color: var(--ink);
    }

    .nav-brand {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      text-decoration: none;
      color: inherit;
      flex-shrink: 0;
    }

    .nav-logo-mark {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: rgba(255,255,255,0.22);
      display: flex;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(8px);
      border: 1.5px solid rgba(255,255,255,0.4);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    #nav.light .nav-logo-mark {
      background: var(--ink);
      border-color: var(--ink);
      color: #fff;
    }

    .nav-logo-mark svg {
      width: 22px;
      height: 22px;
      fill: currentColor;
    }

    .nav-brand-text {
      font-family: 'Inter', sans-serif;
      font-weight: 800;
      font-size: 16.5px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    /* Nav Pill Centered cleanly via Flexbox (no absolute collision) */
    .nav-center-wrap {
      display: flex;
      justify-content: center;
      flex: 1;
      min-width: 0;
    }

    .nav-pill {
      background: rgba(22, 17, 14, 0.75);
      backdrop-filter: blur(18px);
      border: 1.5px solid rgba(255, 255, 255, 0.25);
      border-radius: 99px;
      padding: 5px;
      display: flex;
      align-items: center;
      position: relative;
      box-shadow: 0 8px 24px rgba(0,0,0,0.25);
      flex-shrink: 0;
    }

    #nav.light .nav-pill {
      background: rgba(255, 255, 255, 0.85);
      border-color: rgba(28, 24, 21, 0.2);
      box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }

    .nav-indicator {
      position: absolute;
      top: 5px;
      bottom: 5px;
      left: 5px;
      border-radius: 99px;
      background: #fff;
      transition: all 0.35s var(--ease);
      z-index: 1;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    #nav.light .nav-indicator {
      background: var(--ink);
    }

    .nav-link {
      position: relative;
      z-index: 2;
      padding: 8px 18px;
      font-size: 13.5px;
      font-weight: 500;
      color: inherit;
      text-decoration: none;
      transition: color 0.25s;
      white-space: nowrap;
    }

    .nav-link.active {
      color: var(--ink);
      font-weight: 700;
    }

    #nav.light .nav-link.active {
      color: #fff;
    }

    .nav-right {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }

    .nav-chip {
      padding: 7px 14px;
      border-radius: 99px;
      border: 1.5px solid rgba(255,255,255,0.4);
      background: rgba(255,255,255,0.1);
      font-family: 'DM Mono', monospace;
      font-size: 11px;
      letter-spacing: 0.08em;
      font-weight: 600;
      backdrop-filter: blur(6px);
    }

    #nav.light .nav-chip {
      border-color: rgba(28,24,21,0.25);
      background: rgba(28,24,21,0.05);
      color: var(--ink);
    }

    .nav-cart {
      position: relative;
      width: 44px;
      height: 40px;
      border-radius: 99px;
      background: rgba(255,255,255,0.18);
      border: 1.5px solid rgba(255,255,255,0.35);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: transform 0.2s, background 0.2s;
    }

    .nav-cart:hover {
      transform: scale(1.08);
      background: rgba(255,255,255,0.28);
    }

    #nav.light .nav-cart {
      background: rgba(28,24,21,0.08);
      border-color: rgba(28,24,21,0.2);
      color: var(--ink);
    }

    .nav-cart svg {
      width: 20px;
      height: 20px;
      fill: currentColor;
    }

    .cart-badge {
      position: absolute;
      top: -5px;
      right: -5px;
      background: #e63946;
      color: #fff;
      font-family: 'DM Mono', monospace;
      font-size: 11px;
      padding: 2px 6px;
      border-radius: 99px;
      border: 2px solid #fff;
      font-weight: 700;
      transform: scale(0);
      transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }

    .cart-badge.show {
      transform: scale(1);
    }

    /* WhatsApp Button in Nav (High Contrast, Impossible to Miss) */
    .nav-wa-btn {
      padding: 9px 20px;
      border-radius: 99px;
      background: var(--wa-green) !important;
      color: #fff !important;
      font-weight: 700;
      font-size: 13.5px;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 16px rgba(37, 211, 102, 0.45);
      transition: transform 0.2s var(--ease), background 0.2s, box-shadow 0.2s;
      cursor: pointer;
      border: none;
    }

    .nav-wa-btn:hover {
      transform: scale(1.06);
      background: var(--wa-hover) !important;
      box-shadow: 0 6px 22px rgba(37, 211, 102, 0.65);
    }

    .nav-wa-btn svg {
      width: 18px;
      height: 18px;
      fill: currentColor;
      flex-shrink: 0;
    }

    /* Floating WhatsApp Button for Instant Mobile/Desktop Access */
    .float-wa-btn {
      position: fixed;
      bottom: 28px;
      right: 28px;
      z-index: 95;
      width: 58px;
      height: 58px;
      border-radius: 50%;
      background: var(--wa-green);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 8px 25px rgba(37, 211, 102, 0.55), 0 4px 10px rgba(0,0,0,0.3);
      text-decoration: none;
      cursor: pointer;
      transition: transform 0.25s var(--ease), box-shadow 0.25s;
    }

    .float-wa-btn:hover {
      transform: scale(1.12);
      box-shadow: 0 12px 32px rgba(37, 211, 102, 0.75), 0 6px 14px rgba(0,0,0,0.35);
    }

    .float-wa-btn svg {
      width: 32px;
      height: 32px;
      fill: currentColor;
    }

    .float-wa-tooltip {
      position: absolute;
      right: 70px;
      background: rgba(22, 17, 14, 0.95);
      color: #fff;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
      pointer-events: none;
      opacity: 0;
      transform: translateX(10px);
      transition: all 0.25s ease;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      border: 1px solid rgba(255,255,255,0.15);
    }

    .float-wa-btn:hover .float-wa-tooltip {
      opacity: 1;
      transform: translateX(0);
    }

    /* SECTION 1: HERO (#flavors) */
    #flavors {
      position: relative;
      width: 100vw;
      height: 100svh;
      min-height: 600px;
      background-color: var(--flav);
      overflow: hidden;
      transition: background-color 0.4s ease;
      z-index: 1;
    }

    .reveal {
      position: absolute;
      inset: 0;
      background-color: var(--rv);
      pointer-events: none;
      z-index: 0;
    }

    .rings {
      position: absolute;
      top: 41%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: calc(2200 * var(--u));
      height: calc(2200 * var(--u));
      background: repeating-radial-gradient(circle, rgba(255,255,255,0.13) 0, rgba(255,255,255,0.02) calc(40 * var(--u)), rgba(255,255,255,0.13) calc(80 * var(--u)));
      mask-image: radial-gradient(circle, #000 0 22%, rgba(0,0,0,0.55) 34%, transparent 52%);
      -webkit-mask-image: radial-gradient(circle, #000 0 22%, rgba(0,0,0,0.55) 34%, transparent 52%);
      pointer-events: none;
      z-index: 1;
      opacity: 0.9;
    }

    .bits {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 1;
    }

    .bit {
      position: absolute;
      opacity: 0.7;
      filter: blur(1px);
      transition: transform 0.8s ease-out;
    }

    .arc {
      position: absolute;
      inset: 0;
      z-index: 55;
      touch-action: pan-y;
      cursor: grab;
    }

    #title {
      position: absolute;
      top: calc(50% + 250 * var(--u));
      left: 50%;
      transform: translateX(-50%);
      font-size: min(calc(84 * var(--u)), calc(760 * var(--u) * 100 / 680));
      color: #fff;
      text-align: center;
      z-index: 60;
      pointer-events: none;
      text-shadow: 0 4px 22px rgba(0,0,0,0.4), 0 1px 3px rgba(0,0,0,0.6);
      display: flex;
      gap: 16px;
      justify-content: center;
      flex-wrap: wrap;
    }

    .word {
      display: inline-block;
      white-space: nowrap;
    }

    .letter {
      display: inline-block;
      transform: translateY(0);
      opacity: 1;
      transition: transform 0.5s var(--ease), opacity 0.4s var(--ease);
    }

    .letter.out {
      transform: translateY(-110%);
      opacity: 0;
    }

    .letter.in-prep {
      transform: translateY(110%);
      opacity: 0;
    }

    #count {
      position: absolute;
      top: calc(50% + 180 * var(--u));
      right: calc(50% - 660 * var(--u));
      font-size: calc(180 * var(--u));
      color: transparent;
      -webkit-text-stroke: 2.5px rgba(255,255,255,0.9);
      z-index: 1;
      pointer-events: none;
      line-height: 1;
      transition: transform 0.3s ease, opacity 0.3s ease;
    }

    #play {
      position: absolute;
      top: calc(50% + 195 * var(--u));
      left: 50%;
      transform: translate(-50%, -50%);
      width: calc(56 * var(--u));
      height: calc(56 * var(--u));
      min-width: 46px;
      min-height: 46px;
      border-radius: 50%;
      background: #fff;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      border: none;
      cursor: pointer;
      z-index: 60;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s var(--ease), box-shadow 0.2s;
    }

    #play:hover {
      transform: translate(-50%, -50%) scale(1.1);
      box-shadow: 0 12px 30px rgba(0,0,0,0.4);
    }

    #play svg {
      width: 20px;
      height: 20px;
      fill: var(--ink);
      transform: translateX(1px);
    }

    #auto {
      position: absolute;
      top: calc(50% + 190 * var(--u));
      right: calc(50% - 590 * var(--u));
      z-index: 60;
      background: rgba(18, 14, 11, 0.4);
      border: 1px solid rgba(255,255,255,0.35);
      padding: 6px 14px;
      border-radius: 99px;
      backdrop-filter: blur(6px);
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      font-family: 'DM Mono', monospace;
      font-size: 11px;
      letter-spacing: 0.14em;
      transition: background 0.2s;
    }

    #auto:hover {
      background: rgba(18, 14, 11, 0.7);
    }

    .auto-ring {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      border: 1.5px solid #fff;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .auto-ring svg {
      width: 10px;
      height: 10px;
      fill: #fff;
    }

    /* SECTION 2: INSIDE (#inside) */
    #inside {
      position: relative;
      height: 500vh;
      background-color: var(--flav);
      transition: background-color 0.4s ease;
      z-index: 1;
    }

    .pin {
      position: sticky;
      top: 0;
      height: 100svh;
      width: 100vw;
      overflow: hidden;
    }

    .in-dark {
      position: absolute;
      inset: 0;
      background: #0d0a08;
      opacity: 0;
      pointer-events: none;
      z-index: 1;
      transition: opacity 0.1s linear;
    }

    .in-back-frame {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 1440px;
      height: 900px;
      pointer-events: none;
      z-index: 1;
    }

    .in-num {
      position: absolute;
      top: 140px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 380px;
      color: transparent;
      -webkit-text-stroke: 2.5px rgba(255, 255, 255, 0.45);
      line-height: 1;
      text-align: center;
      transition: opacity 0.3s ease;
    }

    #inBar {
      position: absolute;
      top: 130px;
      left: 630px;
      width: 320px;
      height: 640px;
    }

    /* Fixed front layer for Section 2:
       Controlled via translateY(pinY) so it behaves like sticky and disappears outside Section 2 */
    #inFront {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100svh;
      z-index: 3;
      pointer-events: none;
      display: flex;
      align-items: center;
      justify-content: center;
      will-change: transform, opacity;
    }

    .in-front-frame {
      position: relative;
      width: 1440px;
      height: 900px;
      pointer-events: none;
    }

    .in-head {
      position: absolute;
      top: 290px;
      left: 70px;
      font-size: 78px;
      color: #fff;
      line-height: 0.94;
      text-shadow: 0 4px 24px rgba(0,0,0,0.55), 0 2px 6px rgba(0,0,0,0.6);
      transition: opacity 0.25s ease;
    }

    /* Highly Visible High-Contrast Step Buttons (Fixes Screenshot 2) */
    .in-icons {
      position: absolute;
      top: 280px;
      right: 70px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      pointer-events: auto;
    }

    .in-icon-btn {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      border: 2px solid rgba(255, 255, 255, 0.5);
      background: rgba(22, 17, 14, 0.88);
      backdrop-filter: blur(14px);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: #fff;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45), 0 2px 6px rgba(0,0,0,0.3);
      transition: all 0.25s var(--ease);
      position: relative;
    }

    .in-icon-btn:hover {
      transform: scale(1.12);
      border-color: #fff;
      background: rgba(35, 26, 21, 0.95);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.55);
    }

    .in-icon-btn.active {
      background: #c8963e;
      color: #1a1410;
      border-color: #fff;
      box-shadow: 0 0 25px rgba(200, 150, 62, 0.85), 0 8px 20px rgba(0,0,0,0.5);
    }

    .in-icon-btn svg {
      width: 26px;
      height: 26px;
      fill: currentColor;
    }

    .in-icon-tooltip {
      position: absolute;
      right: 76px;
      background: rgba(22, 17, 14, 0.95);
      color: #fff;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-family: 'DM Mono', monospace;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      white-space: nowrap;
      opacity: 0;
      transform: translateX(10px);
      transition: all 0.25s ease;
      pointer-events: none;
      border: 1px solid rgba(255,255,255,0.2);
      box-shadow: 0 4px 14px rgba(0,0,0,0.35);
    }

    .in-icon-btn:hover .in-icon-tooltip {
      opacity: 1;
      transform: translateX(0);
    }

    /* High-contrast caption card */
    .in-cap {
      position: absolute;
      top: 590px;
      right: 70px;
      width: 340px;
      text-align: right;
      font-size: 13.5px;
      line-height: 1.6;
      color: #fff;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      background: rgba(18, 14, 11, 0.82);
      padding: 14px 20px;
      border-radius: 14px;
      border: 1.5px solid rgba(255,255,255,0.25);
      backdrop-filter: blur(12px);
      box-shadow: 0 8px 24px rgba(0,0,0,0.4);
      transition: opacity 0.25s ease;
    }

    /* Wood storm layer */
    .storm-layer {
      position: absolute;
      inset: 0;
      pointer-events: none;
      overflow: hidden;
    }

    .storm-chip {
      position: absolute;
      opacity: 0;
      transform-origin: center;
      filter: drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    }

    /* SECTION 3: SHOP (#shop) */
    #shop {
      position: relative;
      background: var(--cream);
      padding: calc(96 * var(--w)) calc(48 * var(--w)) calc(80 * var(--w));
      min-height: 100vh;
      z-index: 1;
    }

    .shop-header {
      position: relative;
      margin-bottom: calc(48 * var(--w));
    }

    .shop-headline {
      font-size: calc(88 * var(--w));
      line-height: 0.88;
      color: var(--ink);
    }

    .shop-caption {
      position: absolute;
      right: 0;
      bottom: 12px;
      max-width: calc(380 * var(--w));
      font-size: calc(14.5 * var(--w));
      line-height: 1.5;
      color: #63574e;
    }

    .shop-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: calc(18 * var(--w));
      perspective: 1200px;
    }

    .card {
      position: relative;
      height: calc(450 * var(--w));
      border-radius: calc(22 * var(--w));
      background: var(--wood-color);
      transform-style: preserve-3d;
      padding: calc(24 * var(--w));
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      color: #fff;
      cursor: pointer;
      box-shadow: 0 16px 36px rgba(30,20,15,0.14);
      transition: transform 0.2s var(--ease), box-shadow 0.2s;
    }

    .card:hover {
      box-shadow: 0 24px 44px rgba(30,20,15,0.25);
    }

    .card-title {
      font-size: calc(24 * var(--w));
      line-height: 1.05;
      color: #fff;
      text-shadow: 0 2px 8px rgba(0,0,0,0.25);
    }

    .card-tag {
      font-family: 'DM Mono', monospace;
      font-size: calc(11 * var(--w));
      letter-spacing: 0.12em;
      text-transform: uppercase;
      opacity: 0.9;
      margin-top: 6px;
    }

    .card-pk {
      position: absolute;
      top: calc(88 * var(--w));
      left: 50%;
      transform: translateX(-50%) translateZ(30px);
      width: calc(170 * var(--w));
      height: calc(212 * var(--w));
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 12px 28px rgba(0,0,0,0.3);
      background: rgba(0,0,0,0.12);
    }

    .card-pk img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    /* Live card hides its 2D image so the 3D piece lands right there */
    .card.live .card-pk img {
      visibility: hidden;
    }

    .card-bottom {
      display: flex;
      align-items: center;
      justify-content: space-between;
      transform: translateZ(40px);
      gap: 8px;
    }

    .card-price {
      font-family: 'DM Mono', monospace;
      font-size: calc(18 * var(--w));
      font-weight: 700;
      color: #fff;
      text-shadow: 0 1px 4px rgba(0,0,0,0.3);
    }

    .card-actions-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Direct WhatsApp button per product */
    .card-wa-btn {
      padding: 8px 12px;
      border-radius: 99px;
      background: var(--wa-green);
      color: #fff;
      font-size: calc(12 * var(--w));
      font-weight: 700;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4);
      transition: transform 0.2s, background 0.2s;
    }

    .card-wa-btn:hover {
      transform: scale(1.08);
      background: var(--wa-hover);
    }

    .card-wa-btn svg {
      width: 14px;
      height: 14px;
      fill: currentColor;
    }

    .card-add {
      width: calc(40 * var(--w));
      height: calc(40 * var(--w));
      min-width: 36px;
      min-height: 36px;
      border-radius: 50%;
      background: var(--ink);
      border: 2px solid #fff;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: transform 0.2s, background 0.2s;
    }

    .card-add:hover {
      transform: scale(1.14);
      background: #000;
    }

    .card-add svg {
      width: 16px;
      height: 16px;
      fill: #fff;
    }

    /* SECTION 4: BUILDER / RANGE (#range) */
    #range {
      position: relative;
      background: var(--dark);
      color: var(--cream);
      padding: calc(96 * var(--w)) calc(50 * var(--w)) calc(100 * var(--w));
      min-height: 100vh;
      overflow: hidden;
      z-index: 1;
    }

    .builder-glow {
      position: absolute;
      top: calc(120 * var(--w));
      left: calc(680 * var(--w));
      width: calc(640 * var(--w));
      height: calc(640 * var(--w));
      border-radius: 50%;
      background: radial-gradient(circle, var(--g, rgba(139, 87, 66, 0.72)) 0, rgba(139, 87, 66, 0.25) 35%, transparent 68%);
      filter: blur(40px);
      pointer-events: none;
      transition: background 0.5s ease;
    }

    .builder-headline {
      font-size: calc(68 * var(--w));
      line-height: 0.94;
      margin-bottom: calc(48 * var(--w));
    }

    .builder-badge {
      display: inline-block;
      background: var(--cream);
      color: var(--dark);
      padding: 0 12px;
      border-radius: 12px;
    }

    .builder-slots-container {
      position: relative;
      width: 100%;
      max-width: calc(680 * var(--w));
      height: calc(340 * var(--w));
      margin: 0 auto calc(40 * var(--w));
    }

    .pack-slot {
      position: absolute;
      width: calc(160 * var(--w));
      height: calc(200 * var(--w));
      border-radius: 18px;
      border: 2px dashed rgba(255,255,255,0.3);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(8px);
      transition: all 0.3s var(--ease);
    }

    .pack-slot.slot-0 { top: 10%; left: 38%; }
    .pack-slot.slot-1 { top: 40%; left: 16%; }
    .pack-slot.slot-2 { top: 40%; left: 60%; }

    .pack-slot.filled {
      border-style: solid;
      border-color: rgba(255,255,255,0.5);
      background: rgba(255,255,255,0.1);
    }

    .slot-remove {
      position: absolute;
      top: -12px;
      right: -12px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--ink);
      border: 2px solid var(--cream);
      color: #fff;
      display: none;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 16px;
      font-weight: bold;
      z-index: 5;
    }

    .pack-slot.filled .slot-remove {
      display: flex;
    }

    .slot-img {
      width: 80%;
      height: 80%;
      object-fit: cover;
      border-radius: 10px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }

    .slot-empty-label {
      font-family: 'DM Mono', monospace;
      font-size: calc(11 * var(--w));
      color: rgba(255,255,255,0.6);
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }

    .thumbs-row {
      display: flex;
      gap: calc(20 * var(--w));
      justify-content: center;
      margin-bottom: calc(36 * var(--w));
    }

    .thumb-btn {
      width: calc(110 * var(--w));
      border-radius: 16px;
      background: rgba(255,255,255,0.08);
      border: 1.5px solid rgba(255,255,255,0.2);
      padding: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      transition: transform 0.2s, background 0.2s, border-color 0.2s;
      position: relative;
    }

    .thumb-btn:hover {
      transform: translateY(-4px);
      background: rgba(255,255,255,0.16);
      border-color: #fff;
    }

    .thumb-btn img {
      width: calc(64 * var(--w));
      height: calc(80 * var(--w));
      object-fit: cover;
      border-radius: 8px;
      margin-bottom: 8px;
    }

    .thumb-btn-name {
      font-size: calc(10 * var(--w));
      font-weight: 700;
      text-align: center;
      text-transform: uppercase;
      color: #fff;
      line-height: 1.2;
    }

    .thumb-badge {
      position: absolute;
      top: -6px;
      right: -6px;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: var(--wa-green);
      color: #fff;
      font-family: 'DM Mono', monospace;
      font-size: 11px;
      display: none;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      border: 2px solid #fff;
    }

    .builder-actions {
      display: flex;
      gap: 16px;
      justify-content: center;
      flex-wrap: wrap;
    }

    #buy {
      height: calc(56 * var(--w));
      min-height: 48px;
      padding: 0 calc(36 * var(--w));
      border-radius: 99px;
      background: var(--cream);
      color: var(--dark);
      border: none;
      font-weight: 700;
      font-size: calc(15 * var(--w));
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 16px;
      transition: all 0.3s var(--ease);
    }

    #buy:disabled {
      opacity: 0.35;
      cursor: not-allowed;
    }

    #buy:not(:disabled):hover {
      transform: scale(1.05);
      background: #fff;
      box-shadow: 0 12px 30px rgba(0,0,0,0.3);
    }

    #buy.added {
      background: #4a8063;
      color: #fff;
    }

    #buyWa {
      height: calc(56 * var(--w));
      min-height: 48px;
      padding: 0 calc(32 * var(--w));
      border-radius: 99px;
      background: var(--wa-green);
      color: #fff;
      font-weight: 700;
      font-size: calc(15 * var(--w));
      display: none;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);
      transition: all 0.3s var(--ease);
    }

    #buyWa:hover {
      background: var(--wa-hover);
      transform: scale(1.05);
      box-shadow: 0 8px 24px rgba(37, 211, 102, 0.6);
    }

    #buyWa svg {
      width: 22px;
      height: 22px;
      fill: currentColor;
    }

    /* Fly-to-cart clones */
    .fly-clone {
      position: fixed;
      z-index: 70;
      pointer-events: none;
      border-radius: 12px;
      box-shadow: 0 12px 32px rgba(0,0,0,0.4);
      transition: transform 0.9s cubic-bezier(.5, 0, .2, 1), opacity 0.9s ease;
    }

    /* Responsive / Mobile Rules (Addresses Screenshot 1 and 2) */
    @media (max-width: 1200px) {
      .nav-chip {
        display: none;
      }
    }

    @media (max-width: 980px) {
      .nav-brand-text {
        display: none;
      }
      .nav-link {
        padding: 6px 14px;
        font-size: 12px;
      }
      .shop-grid {
        grid-template-columns: repeat(3, 1fr);
      }
    }

    @media (max-width: 820px) {
      #nav {
        height: 64px;
        padding: 0 16px;
      }
      .nav-brand-text {
        display: none;
      }
      .nav-center-wrap {
        display: none; /* Pill moves to fixed bottom bar on mobile */
      }
      .nav-wa-btn span {
        display: none; /* Show icon only in header to save space */
      }
      .nav-wa-btn {
        width: 38px;
        height: 38px;
        padding: 0;
        justify-content: center;
      }
      .nav-wa-btn svg {
        width: 20px;
        height: 20px;
      }
      .nav-pill-mobile {
        position: fixed;
        bottom: 16px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(22, 17, 14, 0.92);
        backdrop-filter: blur(16px);
        border: 1.5px solid rgba(255,255,255,0.3);
        border-radius: 99px;
        padding: 4px;
        display: flex;
        z-index: 60;
        box-shadow: 0 8px 30px rgba(0,0,0,0.5);
      }
      .nav-pill-mobile .nav-link {
        padding: 6px 12px;
        font-size: 11.5px;
        color: #fff;
      }
      .nav-pill-mobile .nav-link.active {
        color: var(--ink);
        background: #fff;
        border-radius: 99px;
      }

      /* Hero responsive */
      #title {
        font-size: clamp(28px, 8.5vw, 44px);
        top: calc(50% + 200px);
        width: 90vw;
      }
      #count {
        top: 76px;
        right: 18px;
        font-size: 60px;
      }
      #play {
        top: calc(50% + 140px);
        width: 44px;
        height: 44px;
      }
      #auto {
        top: 135px;
        right: 18px;
        font-size: 10px;
        padding: 4px 10px;
      }

      /* Section 2 Mobile Fix: Avoid collision with top header & piece */
      .in-head {
        font-size: 30px !important;
        left: 16px !important;
        top: 80px !important;
        line-height: 1.05 !important;
        text-shadow: 0 3px 12px rgba(0,0,0,0.8) !important;
      }
      .in-icons {
        right: 16px !important;
        top: 80px !important;
        gap: 10px !important;
      }
      .in-icon-btn {
        width: 46px !important;
        height: 46px !important;
      }
      .in-icon-btn svg {
        width: 20px !important;
        height: 20px !important;
      }
      .in-icon-tooltip {
        display: none !important;
      }
      .in-cap {
        right: 16px !important;
        left: 16px !important;
        bottom: 84px !important;
        top: auto !important;
        width: auto !important;
        text-align: center !important;
        font-size: 11.5px !important;
        padding: 10px 14px !important;
      }

      /* Shop responsive */
      .shop-grid {
        display: flex;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        padding-bottom: 20px;
      }
      .card {
        min-width: 280px;
        height: 420px;
        scroll-snap-align: center;
      }
      .builder-slots-container {
        height: 260px;
      }
      .pack-slot {
        width: 110px;
        height: 140px;
      }
      .thumbs-row {
        flex-wrap: wrap;
      }
      .thumb-btn {
        width: 90px;
      }
      .float-wa-btn {
        bottom: 74px;
        right: 16px;
        width: 50px;
        height: 50px;
      }
      .float-wa-btn svg {
        width: 26px;
        height: 26px;
      }
    }
  </style>
</head>
<body class="locked">

  <!-- Three.js Canvas -->
  <canvas id="gl"></canvas>

  <!-- Intro Screen -->
  <div id="intro">
    <div class="intro-rings"></div>
    <div class="intro-stamp">
      <div class="intro-logo-box">
        <svg viewBox="0 0 24 24">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
        </svg>
      </div>
      <h1 class="intro-title">SUPERPERSONALIZADO</h1>
      <p class="intro-sub">Corte Láser & Arte en Madera 3D</p>
    </div>
    <button class="skip-pill" id="skipIntro">
      <span>Saltar Intro</span>
      <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
        <polygon points="5 4 15 12 5 20 5 4"></polygon>
        <line x1="19" y1="5" x2="19" y2="19" stroke="currentColor" stroke-width="2"></line>
      </svg>
    </button>
  </div>

  <!-- Header Nav (Flexbox: Brand, Pill, Actions) -->
  <nav id="nav">
    <a href="#flavors" class="nav-brand">
      <div class="nav-logo-mark">
        <svg viewBox="0 0 24 24">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
        </svg>
      </div>
      <span class="nav-brand-text">Superpersonalizado</span>
    </a>

    <div class="nav-center-wrap">
      <div class="nav-pill" id="navPill">
        <div class="nav-indicator" id="navIndicator"></div>
        <a href="#flavors" class="nav-link active" data-target="flavors">Colección</a>
        <a href="#inside" class="nav-link" data-target="inside">Anatomía</a>
        <a href="#shop" class="nav-link" data-target="shop">Catálogo</a>
        <a href="#range" class="nav-link" data-target="range">Arma tu Pack</a>
      </div>
    </div>

    <div class="nav-right">
      <div class="nav-chip">15% DCTO EN PACKS</div>
      <div class="nav-cart" id="navCart" aria-label="Carrito de compras">
        <svg viewBox="0 0 24 24">
          <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4zM3 6h18M16 10a4 4 0 0 1-8 0"/>
        </svg>
        <div class="cart-badge" id="cartBadge">0</div>
      </div>
      <!-- WhatsApp Direct Action Button in Nav -->
      <a href="https://wa.me/584127588395?text=%C2%A1Hola%21%20Me%20interesa%20personalizar%20un%20producto%20en%20madera%20con%20Superpersonalizado." target="_blank" class="nav-wa-btn" aria-label="Escríbenos a WhatsApp">
        <svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41h-.01c-1.49 0-2.96-.4-4.23-1.15l-.3-.18-3.14.82.84-3.06-.2-.31a8.21 8.21 0 0 1-1.26-4.37c0-4.54 3.7-8.24 8.24-8.24m4.52 11.66c-.25-.12-1.47-.72-1.7-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.17-.25.25-.41.08-.17.04-.31-.02-.43s-.56-1.34-.76-1.84c-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.84-.86 2.05 0 1.21.88 2.38 1 2.54.12.17 1.74 2.65 4.21 3.72.59.25 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.15-1.18-.06-.11-.23-.17-.48-.29"/></svg>
        <span>WhatsApp</span>
      </a>
    </div>
  </nav>

  <!-- Mobile Bottom Pill Navigation -->
  <div class="nav-pill-mobile" id="navPillMobile" style="display: none;">
    <a href="#flavors" class="nav-link active" data-target="flavors">Colección</a>
    <a href="#inside" class="nav-link" data-target="inside">Anatomía</a>
    <a href="#shop" class="nav-link" data-target="shop">Catálogo</a>
    <a href="#range" class="nav-link" data-target="range">Pack</a>
  </div>

  <!-- Floating WhatsApp Quick Button -->
  <a href="https://wa.me/584127588395?text=%C2%A1Hola%21%20Me%20gustar%C3%ADa%20m%C3%A1s%20informaci%C3%B3n%20sobre%20sus%20productos%20en%20madera." target="_blank" class="float-wa-btn" aria-label="Escríbenos a WhatsApp">
    <svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41h-.01c-1.49 0-2.96-.4-4.23-1.15l-.3-.18-3.14.82.84-3.06-.2-.31a8.21 8.21 0 0 1-1.26-4.37c0-4.54 3.7-8.24 8.24-8.24m4.52 11.66c-.25-.12-1.47-.72-1.7-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.17-.25.25-.41.08-.17.04-.31-.02-.43s-.56-1.34-.76-1.84c-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.84-.86 2.05 0 1.21.88 2.38 1 2.54.12.17 1.74 2.65 4.21 3.72.59.25 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.15-1.18-.06-.11-.23-.17-.48-.29"/></svg>
    <span class="float-wa-tooltip">¿Dudas? ¡Escríbenos a WhatsApp!</span>
  </a>

  <!-- SECTION 1: HERO CAROUSEL -->
  <section id="flavors">
    <div class="reveal" id="reveal"></div>
    <div class="rings"></div>
    <div class="bits" id="heroBits"></div>
    <div class="arc" id="arcHit"></div>

    <h1 id="title" class="disp" aria-live="polite">
      <!-- Letters inserted dynamically -->
    </h1>

    <div id="count" class="disp">01</div>

    <button id="play" aria-label="Siguiente modelo">
      <svg viewBox="0 0 24 24">
        <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      </svg>
    </button>

    <button id="auto" aria-pressed="true">
      <div class="auto-ring">
        <svg viewBox="0 0 24 24">
          <rect x="6" y="4" width="4" height="16" rx="1"/>
          <rect x="14" y="4" width="4" height="16" rx="1"/>
        </svg>
      </div>
      <span>AUTOPLAY</span>
    </button>
  </section>

  <!-- SECTION 2: INSIDE (PINNED 3D FLIP) -->
  <section id="inside">
    <div class="pin" id="pin">
      <div class="in-dark" id="inDark"></div>
      <div class="in-back-frame">
        <div class="in-num disp" id="inNum">01</div>
        <div id="inBar"></div>
      </div>
    </div>
  </section>

  <!-- Section 2 Front Fixed Layer (z-index 3) -->
  <div id="inFront">
    <div class="in-front-frame">
      <h2 class="in-head disp" id="inHead">DISEÑO &<br>VECTORIZACIÓN</h2>
      <div class="in-icons">
        <button class="in-icon-btn active" data-step="0" aria-label="Paso 1: Diseño">
          <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          <span class="in-icon-tooltip">Paso 1: Diseño</span>
        </button>
        <button class="in-icon-btn" data-step="1" aria-label="Paso 2: Corte Láser">
          <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 2v3m0 14v3M2 12h3m14 0h3"/></svg>
          <span class="in-icon-tooltip">Paso 2: Corte Láser</span>
        </button>
        <button class="in-icon-btn" data-step="2" aria-label="Paso 3: Ensamble">
          <svg viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
          <span class="in-icon-tooltip">Paso 3: Ensamble</span>
        </button>
        <button class="in-icon-btn" data-step="3" aria-label="Paso 4: Certificación">
          <svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          <span class="in-icon-tooltip">Paso 4: Calidad</span>
        </button>
      </div>
      <p class="in-cap mono" id="inCap">Cada pieza nace de un trazo digital único milimétrico con tolerancias exactas.</p>
    </div>
    <div class="storm-layer" id="stormLayer"></div>
  </div>

  <!-- SECTION 3: SHOP (#shop) -->
  <section id="shop">
    <div class="shop-header">
      <h2 class="shop-headline disp">CATÁLOGO<br>EXCLUSIVO</h2>
      <p class="shop-caption mono">Piezas únicas cortadas al milímetro con láser de alta precisión y ensambladas artesanalmente a mano en nuestro taller.</p>
    </div>

    <div class="shop-grid" id="shopGrid">
      <!-- Generated Cards -->
    </div>
  </section>

  <!-- SECTION 4: BUILDER (#range) -->
  <section id="range">
    <div class="builder-glow" id="builderGlow"></div>
    <div class="shop-header">
      <h2 class="builder-headline disp">ARMA TU PACK<br><span class="builder-badge">[3]</span> PIEZAS &<br>AHORRA 15%</h2>
    </div>

    <div class="builder-slots-container">
      <div class="pack-slot slot-0" id="slot0">
        <button class="slot-remove" data-slot="0">×</button>
        <span class="slot-empty-label">Espacio 1</span>
      </div>
      <div class="pack-slot slot-1" id="slot1">
        <button class="slot-remove" data-slot="1">×</button>
        <span class="slot-empty-label">Espacio 2</span>
      </div>
      <div class="pack-slot slot-2" id="slot2">
        <button class="slot-remove" data-slot="2">×</button>
        <span class="slot-empty-label">Espacio 3</span>
      </div>
    </div>

    <div class="thumbs-row" id="thumbsRow">
      <!-- Product Thumbnails -->
    </div>

    <div class="builder-actions">
      <button id="buy" disabled>
        <span>COMPLETA TU PACK (3 RESTANTES)</span>
        <span class="mono" id="buyPrice">$89.990</span>
      </button>
      <a href="https://wa.me/584127588395" target="_blank" id="buyWa">
        <svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41h-.01c-1.49 0-2.96-.4-4.23-1.15l-.3-.18-3.14.82.84-3.06-.2-.31a8.21 8.21 0 0 1-1.26-4.37c0-4.54 3.7-8.24 8.24-8.24m4.52 11.66c-.25-.12-1.47-.72-1.7-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.17-.25.25-.41.08-.17.04-.31-.02-.43s-.56-1.34-.76-1.84c-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.84-.86 2.05 0 1.21.88 2.38 1 2.54.12.17 1.74 2.65 4.21 3.72.59.25 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.15-1.18-.06-.11-.23-.17-.48-.29"/></svg>
        <span>Pedir Pack por WhatsApp</span>
      </a>
    </div>
  </section>

  <!-- MODULE SCRIPT -->
  <script type="module">
    import * as THREE from 'three';
    import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

    // 1. DATA: Wood products
    const PRODUCTS = [
      {
        id: 'lobo',
        name: 'WALL ART LOBO MULTICAPA',
        color: '#8B5742',
        lightColor: '#A66A52',
        imgUrl: 'assets/images/lobo.webp',
        price: '$34.990',
        tag: 'DECORACIÓN GEOMÉTRICA',
        material: 'MDF Premium & Chapa Cedro Oscuro',
        specs: '7 Capas Superpuestas · 60 × 45 cm',
        dimensions: '600 × 450 × 21 mm'
      },
      {
        id: 'realmadrid',
        name: 'ESCUDO REAL MADRID CON BANNER',
        color: '#B88B4A',
        lightColor: '#D4A359',
        imgUrl: 'assets/images/realmadrid.webp',
        price: '$39.990',
        tag: 'EDICIÓN DEPORTIVA',
        material: 'Madera Roble Dorado & Abedul Báltico',
        specs: 'Relieve 3D · Corona Calada · 55 × 40 cm',
        dimensions: '550 × 400 × 18 mm'
      },
      {
        id: 'rueda',
        name: 'RUEDA DE LA FORTUNA ROMANCE',
        color: '#994D3F',
        lightColor: '#BA6050',
        imgUrl: 'assets/images/rueda.webp',
        price: '$42.990',
        tag: 'MECÁNICA ARTESANAL',
        material: 'Caoba Seleccionada & Okumé',
        specs: 'Estructura Giratoria · 12 Portafotos · 40 × 35 cm',
        dimensions: '400 × 350 × 150 mm'
      },
      {
        id: 'tigre',
        name: 'WALL ART TIGRE VERTICAL',
        color: '#6B4C35',
        lightColor: '#855F43',
        imgUrl: 'assets/images/tigre.webp',
        price: '$36.990',
        tag: 'GEOMETRÍA LOW-POLY',
        material: 'Nogal Rústico Tratado',
        specs: '5 Niveles de Relieve · 70 × 40 cm',
        dimensions: '700 × 400 × 24 mm'
      },
      {
        id: 'portamedallas',
        name: 'PORTAMEDALLAS NATACIÓN',
        color: '#7D533A',
        lightColor: '#996849',
        imgUrl: 'assets/images/portamedallas.webp',
        price: '$31.990',
        tag: 'PERSONALIZACIÓN TOTAL',
        material: 'Teca Pardo Maciza & MDF Hidrófugo',
        specs: 'Soporte 30+ Medallas · Nombre 3D · 65 × 30 cm',
        dimensions: '650 × 300 × 15 mm'
      }
    ];

    const EXTRA_PRODUCTS = [
      { id: 'barcelona', name: 'ESCUDO FC BARCELONA', color: '#883E48', imgUrl: 'assets/images/barcelona.webp', price: '$39.990', tag: 'EDICIÓN CLUB' },
      { id: 'goku_vegeta', name: 'DÍPTICO VEGETA & GOKU', color: '#68503C', imgUrl: 'assets/images/goku_vegeta.webp', price: '$38.990', tag: 'ANIME WOOD ART' },
      { id: 'mama', name: 'PORTAFOTOS TE AMO MAMÁ', color: '#A05844', imgUrl: 'assets/images/mama.webp', price: '$28.990', tag: 'REGALO EMOCIONAL' },
      { id: 'letrero_policia', name: 'LETRERO ESCRITORIO', color: '#5C493B', imgUrl: 'assets/images/letrero_policia.webp', price: '$26.990', tag: 'CORPORATIVO' },
      { id: 'llavero', name: 'LLAVERO ÁRBOL DE LA VIDA', color: '#7E6347', imgUrl: 'assets/images/llavero.webp', price: '$12.990', tag: 'ACCESORIO MADERA' }
    ];

    const SECTION2_STEPS = [
      {
        head: 'DISEÑO &<br>VECTORIZACIÓN',
        cap: 'Cada pieza nace de un trazo digital único milimétrico con tolerancias exactas.',
        angle: 0
      },
      {
        head: 'CORTE LÁSER<br>MULTICAPA',
        cap: 'Corte CO2 asistido por aire. Capas ensambladas con precisión microscópica.',
        angle: 180
      },
      {
        head: 'ACABADO A MANO<br>& SELLADO',
        cap: 'Lijado grano 400 y triple capa de laca poliuretánica satinada protectora.',
        angle: 360
      },
      {
        head: 'PIEZA MAESTRA<br>PERSONALIZADA',
        cap: 'Madera 100% sustentable con certificado de origen de nuestro taller.',
        angle: 720
      }
    ];

    let target = 0;
    let pos = 0;
    let isDragging = false;
    let dragStartX = 0;
    let dragPos0 = 0;
    let velocity = 0;
    let lastDragX = 0;
    let lastDragTime = 0;
    let autoplayActive = true;
    let lastInteraction = performance.now();
    let currentStep = 0;
    let cartCount = 0;
    let packSlots = [null, null, null];

    const body = document.body;
    const canvas = document.getElementById('gl');
    const intro = document.getElementById('intro');
    const skipBtn = document.getElementById('skipIntro');
    const titleEl = document.getElementById('title');
    const countEl = document.getElementById('count');
    const playBtn = document.getElementById('play');
    const autoBtn = document.getElementById('auto');
    const revealEl = document.getElementById('reveal');
    const heroBits = document.getElementById('heroBits');
    const arcHit = document.getElementById('arcHit');
    const nav = document.getElementById('nav');
    const navIndicator = document.getElementById('navIndicator');
    const navPill = document.getElementById('navPill');
    const navPillMobile = document.getElementById('navPillMobile');
    const cartBadge = document.getElementById('cartBadge');
    const inFront = document.getElementById('inFront');
    const inHead = document.getElementById('inHead');
    const inCap = document.getElementById('inCap');
    const inNum = document.getElementById('inNum');
    const inDark = document.getElementById('inDark');
    const inBar = document.getElementById('inBar');
    const stormLayer = document.getElementById('stormLayer');
    const shopGrid = document.getElementById('shopGrid');
    const thumbsRow = document.getElementById('thumbsRow');
    const builderGlow = document.getElementById('builderGlow');
    const buyBtn = document.getElementById('buy');
    const buyWa = document.getElementById('buyWa');

    // 2. PROCEDURAL CANVAS TEXTURE GENERATOR
    function createWoodTextures(product) {
      const W = 640;
      const H = 800;

      const fc = document.createElement('canvas');
      fc.width = W;
      fc.height = H;
      const fctx = fc.getContext('2d');

      const fgrad = fctx.createLinearGradient(0, 0, W, H);
      fgrad.addColorStop(0, product.color);
      fgrad.addColorStop(0.5, product.lightColor);
      fgrad.addColorStop(1, product.color);
      fctx.fillStyle = fgrad;
      fctx.fillRect(0, 0, W, H);

      fctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      for (let y = 0; y < H; y += 4) {
        if (Math.sin(y * 0.1) > 0) {
          fctx.fillRect(0, y, W, 2);
        }
      }

      fctx.strokeStyle = 'rgba(25, 12, 6, 0.85)';
      fctx.lineWidth = 18;
      fctx.strokeRect(9, 9, W - 18, H - 18);

      fctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
      fctx.lineWidth = 3;
      fctx.strokeRect(20, 20, W - 40, H - 40);

      const img = new Image();
      img.src = product.imgUrl;
      img.onload = () => {
        fctx.save();
        fctx.beginPath();
        fctx.roundRect(32, 32, W - 64, H - 110, 24);
        fctx.clip();
        fctx.drawImage(img, 32, 32, W - 64, H - 110);
        fctx.restore();

        fctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
        fctx.font = 'bold 16px Inter, sans-serif';
        fctx.textAlign = 'center';
        fctx.fillText('SUPERPERSONALIZADO · TALLER ARTESANAL', W / 2, H - 45);

        fctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
        fctx.font = '12px "DM Mono", monospace';
        fctx.fillText(product.specs, W / 2, H - 24);

        frontTex.needsUpdate = true;
      };

      const bc = document.createElement('canvas');
      bc.width = W;
      bc.height = H;
      const bctx = bc.getContext('2d');

      const bgrad = bctx.createLinearGradient(0, 0, 0, H);
      bgrad.addColorStop(0, '#362319');
      bgrad.addColorStop(1, '#24160f');
      bctx.fillStyle = bgrad;
      bctx.fillRect(0, 0, W, H);

      bctx.fillStyle = 'rgba(255, 255, 255, 0.03)';
      for (let y = 0; y < H; y += 6) {
        bctx.fillRect(0, y, W, 2);
      }

      bctx.strokeStyle = 'rgba(15, 8, 4, 0.95)';
      bctx.lineWidth = 16;
      bctx.strokeRect(8, 8, W - 16, H - 16);

      bctx.fillStyle = '#f4ede4';
      bctx.font = 'bold 28px "Archivo Black", sans-serif';
      bctx.textAlign = 'center';
      bctx.fillText('SUPERPERSONALIZADO', W / 2, 80);

      bctx.fillStyle = 'rgba(244, 237, 228, 0.7)';
      bctx.font = '13px "DM Mono", monospace';
      bctx.fillText('FICHA TÉCNICA · CONTROL DE CALIDAD', W / 2, 110);

      bctx.fillStyle = 'rgba(244, 237, 228, 0.92)';
      bctx.beginPath();
      bctx.roundRect(40, 140, W - 80, 480, 20);
      bctx.fill();

      bctx.fillStyle = '#1c1815';
      bctx.textAlign = 'left';
      bctx.font = 'bold 18px "Archivo Black", sans-serif';
      bctx.fillText('CERTIFICADO DE AUTENTICIDAD', 70, 190);

      bctx.font = '12px "DM Mono", monospace';
      bctx.fillStyle = '#555';
      bctx.fillText('MODELO: ' + product.name, 70, 220);
      bctx.fillText('MATERIAL: ' + product.material, 70, 250);
      bctx.fillText('DIMENSIONES: ' + product.dimensions, 70, 280);
      bctx.fillText('CORTE: Láser CNC CO2 (Tolerancia ±0.1mm)', 70, 310);
      bctx.fillText('ACABADO: Laca Poliuretánica Mate Satinada', 70, 340);
      bctx.fillText('ORIGEN: Madera FSC 100% Sustentable', 70, 370);
      bctx.fillText('SERIE TALLER: #SP-' + Math.floor(10000 + Math.random() * 90000), 70, 400);

      bctx.strokeStyle = '#ddd';
      bctx.lineWidth = 1.5;
      bctx.beginPath();
      bctx.moveTo(70, 430);
      bctx.lineTo(W - 70, 430);
      bctx.stroke();

      bctx.fillStyle = '#1c1815';
      const barcodeY = 460;
      let bx = 70;
      while (bx < W - 70) {
        const bw = (Math.sin(bx * 0.4) > 0 ? 3 : 1.5);
        bctx.fillRect(bx, barcodeY, bw, 45);
        bx += bw + (Math.cos(bx) > 0 ? 3 : 2);
      }

      bctx.textAlign = 'center';
      bctx.font = '11px "DM Mono", monospace';
      bctx.fillText('MADE IN WORKSHOP · GARANTÍA DE POR VIDA', W / 2, 540);

      bctx.strokeStyle = '#8B5742';
      bctx.lineWidth = 2.5;
      bctx.strokeRect(W / 2 - 80, 565, 160, 32);
      bctx.fillStyle = '#8B5742';
      bctx.font = 'bold 12px "DM Mono", monospace';
      bctx.fillText('CALIDAD VERIFICADA', W / 2, 585);

      bctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
      bctx.font = 'bold 13px "DM Mono", monospace';
      bctx.fillText('EDICIÓN LIMITADA · SUPERPERSONALIZADO.COM', W / 2, H - 45);

      const frontTex = new THREE.CanvasTexture(fc);
      frontTex.colorSpace = THREE.SRGBColorSpace;
      frontTex.anisotropy = 8;

      const backTex = new THREE.CanvasTexture(bc);
      backTex.colorSpace = THREE.SRGBColorSpace;
      backTex.anisotropy = 8;

      return { frontTex, backTex };
    }

    // 3. THREE.JS 3D SCENE SETUP
    const renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: true
    });
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const scene = new THREE.Scene();
    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;

    let D = 1500;
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 10, 8000);
    camera.position.set(0, 0, D);

    function updateCamera() {
      const vw = window.innerWidth;
      const vh = window.innerHeight;
      D = Math.max(1000, Math.min(2200, 1500 * Math.min(vw / 1440, vh / 900)));
      const fov = 2 * Math.atan((vh / 2) / D) * (180 / Math.PI);
      camera.fov = fov;
      camera.aspect = vw / vh;
      camera.position.set(0, 0, D);
      camera.updateProjectionMatrix();
      renderer.setSize(vw, vh, false);

      if (vw <= 820) {
        navPillMobile.style.display = 'flex';
      } else {
        navPillMobile.style.display = 'none';
      }
    }
    updateCamera();
    window.addEventListener('resize', updateCamera);

    const ambientLight = new THREE.AmbientLight(0xfff7ed, 0.65);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xfff5e6, 1.25);
    sunLight.position.set(-0.6, 0.9, 1.4).normalize();
    scene.add(sunLight);

    const rimLight = new THREE.DirectionalLight(0xffffff, 0.45);
    rimLight.position.set(0.6, -0.5, -1.0).normalize();
    scene.add(rimLight);

    const BH = 1.25;

    function createWoodGeometry(isFront) {
      const geom = new THREE.PlaneGeometry(1, BH, 32, 40);
      const posAttr = geom.attributes.position;
      const uvAttr = geom.attributes.uv;

      for (let i = 0; i < posAttr.count; i++) {
        const u = uvAttr.getX(i);
        const v = uvAttr.getY(i);
        const ex = Math.abs(2 * u - 1);
        const ey = Math.abs(2 * v - 1);

        const across = Math.pow(Math.max(0, 1 - Math.pow(ex, 3.2)), 0.65);
        const along = Math.pow(Math.max(0, 1 - Math.pow(ey, 3.2)), 0.65);
        let z = 0.012 + 0.055 * across * along + 0.003 * Math.sin(16 * u + 22 * v) * across;

        if (!isFront) {
          z = -z;
          uvAttr.setX(i, 1 - u);
        }
        posAttr.setZ(i, z);
      }

      if (!isFront) {
        const index = geom.index;
        for (let i = 0; i < index.count; i += 3) {
          const a = index.getX(i);
          const b = index.getX(i + 1);
          index.setX(i, b);
          index.setX(i + 1, a);
        }
      }

      geom.computeVertexNormals();
      return geom;
    }

    const geomFront = createWoodGeometry(true);
    const geomBack = createWoodGeometry(false);

    const shadowCanvas = document.createElement('canvas');
    shadowCanvas.width = 256;
    shadowCanvas.height = 256;
    const sctx = shadowCanvas.getContext('2d');
    const sgrad = sctx.createRadialGradient(128, 128, 10, 128, 128, 120);
    sgrad.addColorStop(0, 'rgba(32, 18, 12, 0.6)');
    sgrad.addColorStop(0.5, 'rgba(32, 18, 12, 0.2)');
    sgrad.addColorStop(1, 'transparent');
    sctx.fillStyle = sgrad;
    sctx.fillRect(0, 0, 256, 256);

    const shadowTex = new THREE.CanvasTexture(shadowCanvas);
    const shadowMat = new THREE.MeshBasicMaterial({
      map: shadowTex,
      transparent: true,
      depthWrite: false
    });
    const shadowGeom = new THREE.PlaneGeometry(1.3, 1.3 * BH);

    const productTextures = PRODUCTS.map(p => createWoodTextures(p));

    function createWoodPieceInstance() {
      const group = new THREE.Group();

      const frontMat = new THREE.MeshPhysicalMaterial({
        roughness: 0.38,
        metalness: 0.04,
        clearcoat: 0.45,
        clearcoatRoughness: 0.28,
        envMapIntensity: 0.55,
        transparent: true
      });

      const backMat = new THREE.MeshPhysicalMaterial({
        roughness: 0.42,
        metalness: 0.04,
        clearcoat: 0.35,
        clearcoatRoughness: 0.32,
        envMapIntensity: 0.45,
        transparent: true
      });

      const frontMesh = new THREE.Mesh(geomFront, frontMat);
      const backMesh = new THREE.Mesh(geomBack, backMat);
      const shadowMesh = new THREE.Mesh(shadowGeom, shadowMat.clone());
      shadowMesh.renderOrder = -1;
      shadowMesh.position.set(0, -0.06 * BH, -0.3);

      group.add(frontMesh);
      group.add(backMesh);
      group.add(shadowMesh);
      scene.add(group);

      return { group, frontMesh, backMesh, frontMat, backMat, shadowMesh };
    }

    const POOL_SIZE = 11;
    const barPool = Array.from({ length: POOL_SIZE }, () => createWoodPieceInstance());
    const traveler = createWoodPieceInstance();

    // 5. SCREEN-TO-WORLD PLACEMENT
    function placeWoodGroup(instance, state) {
      const vw = window.innerWidth;
      const vh = window.innerHeight;
      const { x, y, h, rz, ry, rx, z, op, sx = 1, sy = 1, shadow = 1 } = state;

      if (op <= 0.01 || y + h < -200 || y - h > vh + 200) {
        instance.group.visible = false;
        return;
      }
      instance.group.visible = true;

      instance.group.position.x = x - vw / 2;
      instance.group.position.y = vh / 2 - y;
      instance.group.position.z = z;

      const scale = h / BH;
      instance.group.scale.set(scale * sx, scale * sy, scale);

      instance.group.rotation.order = 'ZYX';
      instance.group.rotation.set(
        (rx || 0) * Math.PI / 180,
        (ry || 0) * Math.PI / 180,
        -(rz || 0) * Math.PI / 180
      );

      instance.frontMat.opacity = op;
      instance.backMat.opacity = op;
      instance.shadowMesh.material.opacity = 0.5 * op * shadow;
      instance.shadowMesh.scale.x = Math.max(0.3, Math.abs(Math.cos((ry || 0) * Math.PI / 180)));
    }

    // 6. ARC GEOMETRY & INTERPOLATION
    const ARC_SLOTS = [
      { k: 0, dx: 0, dy: 0, h: 430, rz: 0, ry: 0 },
      { k: 1, dx: 245, dy: 24, h: 330, rz: 4, ry: 16 },
      { k: 2, dx: 452, dy: 44, h: 312, rz: 8, ry: 26 },
      { k: 3, dx: 660, dy: 80, h: 296, rz: 12, ry: 34 },
      { k: 4, dx: 860, dy: 118, h: 280, rz: 15, ry: 40 }
    ];

    function getArcState(k, unit, heroHeight, now, jIndex, heroTop = 0) {
      const sign = Math.sign(k);
      const ak = Math.min(4, Math.abs(k));
      const i0 = Math.floor(ak);
      const i1 = Math.min(4, i0 + 1);
      const t = ak - i0;

      const s0 = ARC_SLOTS[i0];
      const s1 = ARC_SLOTS[i1];

      const dx = (s0.dx + (s1.dx - s0.dx) * t) * sign * unit;
      const dy = (s0.dy + (s1.dy - s0.dy) * t) * unit;
      const h = (s0.h + (s1.h - s0.h) * t) * unit;
      const rz = (s0.rz + (s1.rz - s0.rz) * t) * sign;
      const ry = (s0.ry + (s1.ry - s0.ry) * t) * sign;

      const cx = window.innerWidth / 2;
      const cy = (window.innerWidth < 820)
        ? heroHeight * 0.40
        : (heroHeight / 2 - 78 * unit);

      let x = cx + dx;
      let y = cy + dy + heroTop;

      const b = Math.sin(now / 4600 * Math.PI * 2 + 1.37 * jIndex);
      y -= (0.5 * b + 0.5) * 9 * unit;
      const bobRz = rz + 0.4 * b;

      const z = -ak * 34 * unit;
      let op = 1;
      if (ak > 3.3) {
        op = Math.max(0, 1 - (ak - 3.3) / (3.9 - 3.3));
      }

      return { x, y, h, rz: bobRz, ry, rx: 0, z, op, shadow: 1 };
    }

    // 7. TITLE & TEXT UPDATES
    function updateHeroText(index, forward = true) {
      const product = PRODUCTS[index];
      countEl.textContent = '0' + (index + 1);

      const words = product.name.split(' ');
      titleEl.innerHTML = '';
      words.forEach(w => {
        const spanWord = document.createElement('span');
        spanWord.className = 'word';
        for (let ch of w) {
          const s = document.createElement('span');
          s.className = 'letter';
          s.textContent = ch;
          spanWord.appendChild(s);
        }
        titleEl.appendChild(spanWord);
      });

      triggerColorReveal(product.color);
    }

    function triggerColorReveal(newColor) {
      document.documentElement.style.setProperty('--rv', newColor);
      revealEl.style.transition = 'clip-path 0.55s cubic-bezier(.25,.75,.2,1)';
      revealEl.style.clipPath = 'circle(150% at 50% 50%)';

      setTimeout(() => {
        document.documentElement.style.setProperty('--flav', newColor);
        revealEl.style.transition = 'none';
        revealEl.style.clipPath = 'circle(0 at 50% 50%)';
        builderGlow.style.background = `radial-gradient(circle, ${newColor} 0, rgba(139, 87, 66, 0.25) 35%, transparent 68%)`;
      }, 550);
    }

    // 8. INTERACTIVE DRAG & NAVIGATION
    let tweenTarget = 0;
    let isTweening = false;
    let tweenStartTime = 0;
    let tweenStartPos = 0;
    let tweenDuration = 650;

    function goTo(newTarget) {
      target = newTarget;
      tweenStartPos = pos;
      tweenTarget = target;
      tweenStartTime = performance.now();
      isTweening = true;
      const count = Math.abs(tweenTarget - tweenStartPos);
      tweenDuration = Math.max(380, 650 * Math.min(1, count + 0.35));

      const activeIdx = ((Math.round(target) % 5) + 5) % 5;
      updateHeroText(activeIdx);
    }

    arcHit.addEventListener('pointerdown', (e) => {
      isDragging = true;
      dragStartX = e.clientX;
      dragPos0 = pos;
      lastDragX = e.clientX;
      lastDragTime = performance.now();
      velocity = 0;
      body.classList.add('dragging');
      arcHit.setPointerCapture(e.pointerId);
      lastInteraction = performance.now();
    });

    arcHit.addEventListener('pointermove', (e) => {
      if (!isDragging) return;
      lastInteraction = performance.now();
      const dx = e.clientX - dragStartX;
      const unit = Math.min(window.innerWidth / 1440, window.innerHeight / 900);
      const slotPx = 245 * unit;
      pos = dragPos0 - dx / slotPx;

      const now = performance.now();
      const dt = now - lastDragTime;
      if (dt > 10) {
        velocity = 0.4 * ((e.clientX - lastDragX) / dt) + 0.6 * velocity;
        lastDragX = e.clientX;
        lastDragTime = now;
      }
    });

    function finishDrag() {
      if (!isDragging) return;
      isDragging = false;
      body.classList.remove('dragging');

      const snapTarget = Math.round(pos - Math.max(-2, Math.min(2, velocity * 180)));
      goTo(snapTarget);
    }

    arcHit.addEventListener('pointerup', finishDrag);
    arcHit.addEventListener('pointercancel', finishDrag);

    playBtn.addEventListener('click', () => {
      lastInteraction = performance.now();
      goTo(target + 1);
    });

    autoBtn.addEventListener('click', () => {
      autoplayActive = !autoplayActive;
      autoBtn.setAttribute('aria-pressed', autoplayActive ? 'true' : 'false');
      autoBtn.querySelector('span').textContent = autoplayActive ? 'AUTOPLAY' : 'PAUSADO';
    });

    // 9. SECTION 2 STEP ICONS
    const stepButtons = document.querySelectorAll('.in-icon-btn');
    stepButtons.forEach((btn, idx) => {
      btn.addEventListener('click', () => {
        const sec2 = document.getElementById('inside');
        const secTop = sec2.offsetTop;
        const secH = sec2.offsetHeight - window.innerHeight;
        const targetScroll = secTop + (idx * 0.22 + 0.05) * secH;
        window.scrollTo({ top: targetScroll, behavior: 'smooth' });
      });
    });

    // 10. WOOD STORM PARTICLES CREATION
    function createStormChips() {
      stormLayer.innerHTML = '';
      for (let i = 0; i < 20; i++) {
        const chip = document.createElement('div');
        chip.className = 'storm-chip';
        chip.style.width = `${Math.floor(40 + Math.random() * 40)}px`;
        chip.style.height = `${Math.floor(40 + Math.random() * 40)}px`;
        chip.style.borderRadius = i % 2 === 0 ? '50%' : '8px';
        chip.style.background = i % 3 === 0 ? '#8B5742' : (i % 3 === 1 ? '#B88B4A' : '#994D3F');
        chip.style.border = '2px solid rgba(25, 12, 6, 0.8)';
        stormLayer.appendChild(chip);
      }
    }
    createStormChips();

    // 11. SHOP SECTION: POPULATE CARDS (With WhatsApp buttons)
    function buildShopGrid() {
      shopGrid.innerHTML = '';
      const allCards = [...PRODUCTS, ...EXTRA_PRODUCTS];
      allCards.forEach((prod, idx) => {
        const card = document.createElement('div');
        card.className = 'card' + (idx === 0 ? ' live' : '');
        card.dataset.index = idx;
        card.style.setProperty('--wood-color', prod.color);

        const waText = encodeURIComponent(`¡Hola! Me interesa este producto: *${prod.name}* (Precio: ${prod.price}). ¿Está disponible? Me gustaría más información.`);
        const waLink = `https://wa.me/584127588395?text=${waText}`;

        card.innerHTML = `
          <div>
            <h3 class="card-title disp">${prod.name}</h3>
            <p class="card-tag">${prod.tag}</p>
          </div>
          <div class="card-pk">
            <img src="${prod.imgUrl}" alt="${prod.name}">
          </div>
          <div class="card-bottom">
            <span class="card-price">${prod.price}</span>
            <div class="card-actions-group">
              <a href="${waLink}" target="_blank" class="card-wa-btn" aria-label="Pedir ${prod.name} por WhatsApp">
                <svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c4.54 0 8.24 3.7 8.24 8.24 0 2.2-.86 4.28-2.42 5.84a8.18 8.18 0 0 1-5.82 2.41h-.01c-1.49 0-2.96-.4-4.23-1.15l-.3-.18-3.14.82.84-3.06-.2-.31a8.21 8.21 0 0 1-1.26-4.37c0-4.54 3.7-8.24 8.24-8.24m4.52 11.66c-.25-.12-1.47-.72-1.7-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.17-.25.25-.41.08-.17.04-.31-.02-.43s-.56-1.34-.76-1.84c-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.84-.86 2.05 0 1.21.88 2.38 1 2.54.12.17 1.74 2.65 4.21 3.72.59.25 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.15-1.18-.06-.11-.23-.17-.48-.29"/></svg>
                <span>Pedir</span>
              </a>
              <button class="card-add" aria-label="Agregar ${prod.name} al carrito">
                <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>
              </button>
            </div>
          </div>
        `;

        card.addEventListener('mousemove', (e) => {
          const rect = card.getBoundingClientRect();
          const x = (e.clientX - rect.left) / rect.width - 0.5;
          const y = (e.clientY - rect.top) / rect.height - 0.5;
          card.style.transform = `translateY(-8px) rotateX(${-y * 12}deg) rotateY(${x * 12}deg)`;
        });
        card.addEventListener('mouseleave', () => {
          card.style.transform = 'translateY(0) rotateX(0) rotateY(0)';
        });

        card.querySelector('.card-add').addEventListener('click', (e) => {
          e.stopPropagation();
          flyToCart(card.querySelector('img'), 1);
        });

        shopGrid.appendChild(card);
      });
    }
    buildShopGrid();

    // 12. BUILDER / PACK CREATION
    function buildPackThumbnails() {
      thumbsRow.innerHTML = '';
      PRODUCTS.forEach((prod, idx) => {
        const btn = document.createElement('div');
        btn.className = 'thumb-btn';
        btn.innerHTML = `
          <div class="thumb-badge" id="thumbBadge${idx}">0</div>
          <img src="${prod.imgUrl}" alt="${prod.name}">
          <span class="thumb-btn-name">${prod.name.split(' ')[0]}</span>
        `;
        btn.addEventListener('click', () => addProductToPack(idx));
        thumbsRow.appendChild(btn);
      });
    }
    buildPackThumbnails();

    function addProductToPack(prodIndex) {
      const emptySlotIdx = packSlots.findIndex(s => s === null);
      if (emptySlotIdx === -1) return;

      packSlots[emptySlotIdx] = prodIndex;
      renderPackSlots();
    }

    function removeProductFromPack(slotIdx) {
      packSlots[slotIdx] = null;
      renderPackSlots();
    }

    document.querySelectorAll('.slot-remove').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const slotIdx = parseInt(btn.dataset.slot);
        removeProductFromPack(slotIdx);
      });
    });

    function renderPackSlots() {
      const counts = [0, 0, 0, 0, 0];
      let filledCount = 0;

      packSlots.forEach((pIdx, slotIdx) => {
        const slotEl = document.getElementById('slot' + slotIdx);
        if (pIdx !== null) {
          filledCount++;
          counts[pIdx]++;
          const prod = PRODUCTS[pIdx];
          slotEl.classList.add('filled');
          slotEl.innerHTML = `
            <button class="slot-remove" data-slot="${slotIdx}">×</button>
            <img class="slot-img" src="${prod.imgUrl}" alt="${prod.name}">
          `;
          slotEl.querySelector('.slot-remove').addEventListener('click', (e) => {
            e.stopPropagation();
            removeProductFromPack(slotIdx);
          });
        } else {
          slotEl.classList.remove('filled');
          slotEl.innerHTML = `
            <button class="slot-remove" data-slot="${slotIdx}">×</button>
            <span class="slot-empty-label">Espacio ${slotIdx + 1}</span>
          `;
        }
      });

      counts.forEach((c, i) => {
        const b = document.getElementById('thumbBadge' + i);
        if (b) {
          b.style.display = c > 0 ? 'flex' : 'none';
          b.textContent = c;
        }
      });

      if (filledCount === 3) {
        buyBtn.disabled = false;
        buyBtn.querySelector('span:first-child').textContent = 'AGREGAR PACK AL CARRITO';
        buyWa.style.display = 'inline-flex';

        // Prepare WhatsApp link for full pack
        const items = packSlots.map((p, i) => `${i + 1}) ${PRODUCTS[p].name}`).join(' | ');
        const waMsg = encodeURIComponent(`¡Hola! Armé mi pack de 3 piezas en Superpersonalizado:\n${items}\nTotal con 15% Descuento: $89.990.\n¿Cómo realizo el pago y envío?`);
        buyWa.href = `https://wa.me/584127588395?text=${waMsg}`;
      } else {
        buyBtn.disabled = true;
        buyBtn.querySelector('span:first-child').textContent = `COMPLETA TU PACK (${3 - filledCount} RESTANTES)`;
        buyWa.style.display = 'none';
      }
    }

    buyBtn.addEventListener('click', () => {
      if (packSlots.some(s => s === null)) return;

      document.querySelectorAll('.pack-slot.filled img').forEach((img, i) => {
        setTimeout(() => flyToCart(img, 1), i * 140);
      });

      buyBtn.classList.add('added');
      buyBtn.querySelector('span:first-child').textContent = '¡PACK AGREGADO!';

      setTimeout(() => {
        packSlots = [null, null, null];
        renderPackSlots();
        buyBtn.classList.remove('added');
      }, 1600);
    });

    // 13. FLY TO CART ANIMATION
    function flyToCart(sourceEl, countToAdd = 1) {
      const rect = sourceEl.getBoundingClientRect();
      const cartRect = document.getElementById('navCart').getBoundingClientRect();

      const clone = sourceEl.cloneNode(true);
      clone.className = 'fly-clone';
      clone.style.left = `${rect.left}px`;
      clone.style.top = `${rect.top}px`;
      clone.style.width = `${rect.width}px`;
      clone.style.height = `${rect.height}px`;
      document.body.appendChild(clone);

      const dx = cartRect.left + cartRect.width / 2 - (rect.left + rect.width / 2);
      const dy = cartRect.top + cartRect.height / 2 - (rect.top + rect.height / 2);

      requestAnimationFrame(() => {
        clone.style.transform = `translate(${dx}px, ${dy}px) scale(0.18) rotate(-18deg)`;
        clone.style.opacity = '0.2';
      });

      setTimeout(() => {
        clone.remove();
        cartCount += countToAdd;
        cartBadge.textContent = cartCount;
        cartBadge.classList.add('show');

        const navCart = document.getElementById('navCart');
        navCart.style.transform = 'scale(1.22)';
        setTimeout(() => navCart.style.transform = 'scale(1)', 240);
      }, 900);
    }

    // 14. INTRO TIMING
    skipBtn.addEventListener('click', closeIntro);

    function closeIntro() {
      intro.classList.add('hidden');
      body.classList.remove('locked');
      goTo(0);
    }
    setTimeout(closeIntro, 3500);

    updateHeroText(0);

    // 15. MAIN ANIMATION FRAME LOOP
    let lastTime = performance.now();

    function render(now) {
      const dt = now - lastTime;
      lastTime = now;

      if (isTweening) {
        const elapsed = now - tweenStartTime;
        const progress = Math.min(1, elapsed / tweenDuration);
        const ease = progress < 0.5
          ? 4 * progress * progress * progress
          : 1 - Math.pow(-2 * progress + 2, 3) / 2;

        pos = tweenStartPos + (tweenTarget - tweenStartPos) * ease;
        if (progress >= 1) {
          isTweening = false;
          pos = tweenTarget;
        }
      }

      if (autoplayActive && !isDragging && !isTweening && (now - lastInteraction > 3200)) {
        if (window.scrollY < window.innerHeight * 0.6) {
          goTo(target + 1);
          lastInteraction = now;
        }
      }

      const activeProductIndex = ((Math.round(pos) % 5) + 5) % 5;
      const unit = Math.min(window.innerWidth / 1440, window.innerHeight / 900);
      const heroEl = document.getElementById('flavors');
      const heroRect = heroEl.getBoundingClientRect();
      const heroHeight = heroEl.offsetHeight;

      const sec2 = document.getElementById('inside');
      const sec2Rect = sec2.getBoundingClientRect();
      const vh = window.innerHeight;

      // Section 2 Sticky Simulation & Culling
      let pinY = 0;
      if (sec2Rect.top > 0) {
        pinY = sec2Rect.top;
      } else if (sec2Rect.bottom < vh) {
        pinY = sec2Rect.bottom - vh;
      } else {
        pinY = 0;
      }
      inFront.style.transform = `translateY(${pinY}px)`;

      const sec2InView = (sec2Rect.bottom > 0 && sec2Rect.top < vh);
      inFront.style.display = sec2InView ? 'flex' : 'none';

      // Hero bars pool: Fades out completely when leaving Hero
      const p1 = Math.max(0, Math.min(1, 1 - sec2Rect.top / vh));
      const heroFade = Math.max(0, 1 - 1.6 * p1);
      const heroBarsVisible = (heroRect.bottom > 0 && heroFade > 0.01);

      const centerJ = Math.floor(pos);
      const jT = Math.round(target);

      for (let i = 0; i < POOL_SIZE; i++) {
        const j = centerJ - 5 + i;
        const inst = barPool[i];

        if (j === jT || !heroBarsVisible) {
          inst.group.visible = false;
          continue;
        }

        const k = j - pos;
        const flavIndex = ((j % 5) + 5) % 5;
        const state = getArcState(k, unit, heroHeight, now, j, heroRect.top);
        state.op *= heroFade;

        inst.frontMesh.material.map = productTextures[flavIndex].frontTex;
        inst.backMesh.material.map = productTextures[flavIndex].backTex;

        placeWoodGroup(inst, state);
      }

      // Section 2 Scroll Mapping
      const pScroll = Math.max(0, Math.min(1, -sec2Rect.top / (sec2.offsetHeight - vh)));

      // Traveler State A: Center of Hero Arc
      const kT = jT - pos;
      const flavT = ((jT % 5) + 5) % 5;
      const stateA = getArcState(kT, unit, heroHeight, now, jT, heroRect.top);

      // Traveler State B: Section 2 InBar placeholder
      const inBarRect = inBar.getBoundingClientRect();
      const inBarCx = inBarRect.left + inBarRect.width / 2;
      const inBarCy = inBarRect.top + inBarRect.height / 2;

      const stepIdx = Math.min(3, Math.floor(Math.min(pScroll, 0.759) / 0.19));
      if (stepIdx !== currentStep && p1 > 0.3) {
        currentStep = stepIdx;
        const stepData = SECTION2_STEPS[currentStep];
        inHead.innerHTML = stepData.head;
        inCap.textContent = stepData.cap;
        inNum.textContent = '0' + (currentStep + 1);

        stepButtons.forEach((b, idx) => {
          b.classList.toggle('active', idx === currentStep);
        });
      }

      const targetAngle = SECTION2_STEPS[stepIdx].angle;
      const stormQ = Math.max(0, Math.min(1, (pScroll - 0.76) / 0.24));
      const ryB = targetAngle + stormQ * 720;

      if (stormQ > 0) {
        const stormFade = Math.max(0, 1 - Math.min(1, 4 * stormQ));
        inHead.style.opacity = stormFade.toString();
        inNum.style.opacity = stormFade.toString();
        inCap.style.opacity = stormFade.toString();
      } else {
        inHead.style.opacity = '1';
        inNum.style.opacity = '1';
        inCap.style.opacity = '1';
      }

      const stateB = {
        x: inBarCx,
        y: inBarCy,
        h: inBarRect.height,
        rz: 14 + Math.sin(now / 2600 * Math.PI * 2) * 2,
        ry: ryB,
        rx: 0,
        z: 40,
        op: 1,
        shadow: 1
      };

      inDark.style.opacity = (stormQ * 0.7).toString();
      const stormChips = document.querySelectorAll('.storm-chip');
      stormChips.forEach((chip, i) => {
        if (stormQ > 0 && stormQ < 1) {
          const angle = (i / 20) * Math.PI * 2;
          const dist = stormQ * Math.min(window.innerWidth, window.innerHeight) * 0.65;
          const cx = window.innerWidth / 2 + Math.cos(angle) * dist;
          const cy = window.innerHeight / 2 + Math.sin(angle) * dist;
          chip.style.opacity = Math.sin(stormQ * Math.PI).toString();
          chip.style.left = `${cx}px`;
          chip.style.top = `${cy}px`;
          chip.style.transform = `rotate(${stormQ * 720}deg) scale(${0.5 + stormQ * 1.2})`;
        } else {
          chip.style.opacity = '0';
        }
      });

      // Traveler State C: Shop Card landing
      const shopEl = document.getElementById('shop');
      const shopRect = shopEl.getBoundingClientRect();
      const p3 = Math.max(0, Math.min(1, (vh - shopRect.top) / (0.7 * vh)));

      document.querySelectorAll('.card').forEach((c, idx) => {
        c.classList.toggle('live', idx === flavT);
      });

      const liveCard = document.querySelector(`.card[data-index="${flavT}"]`);
      let stateC = { ...stateB };
      if (liveCard) {
        const pkRect = liveCard.querySelector('.card-pk').getBoundingClientRect();
        stateC = {
          x: pkRect.left + pkRect.width / 2,
          y: pkRect.top + pkRect.height / 2,
          h: pkRect.height,
          rz: 0,
          ry: Math.round(ryB / 360) * 360,
          rx: 0,
          z: 30,
          op: 1,
          shadow: 0.7
        };
      }

      let finalState = { ...stateA };
      if (p1 > 0 && p3 === 0) {
        const t1 = p1 < 0.5 ? 2 * p1 * p1 : -1 + (4 - 2 * p1) * p1;
        for (let key in stateA) {
          finalState[key] = stateA[key] + (stateB[key] - stateA[key]) * t1;
        }
      } else if (p3 > 0) {
        const t3 = p3 < 0.5 ? 2 * p3 * p3 : -1 + (4 - 2 * p3) * p3;
        for (let key in stateB) {
          finalState[key] = stateB[key] + (stateC[key] - stateB[key]) * t3;
        }
      }

      if (finalState.y + finalState.h / 2 < -50 || finalState.y - finalState.h / 2 > vh + 50) {
        traveler.group.visible = false;
      } else {
        traveler.frontMesh.material.map = productTextures[flavT].frontTex;
        traveler.backMesh.material.map = productTextures[flavT].backTex;
        placeWoodGroup(traveler, finalState);
      }

      renderer.render(scene, camera);
      updateNavHighlight();
      requestAnimationFrame(render);
    }

    // 16. NAV HIGHLIGHT POSITIONING
    function updateNavHighlight() {
      const sections = ['flavors', 'inside', 'shop', 'range'];
      let activeSec = 'flavors';
      const scrollY = window.scrollY;
      const vh = window.innerHeight;

      for (let secId of sections) {
        const el = document.getElementById(secId);
        if (el && el.offsetTop <= scrollY + vh * 0.35) {
          activeSec = secId;
        }
      }

      const activeLink = document.querySelector(`.nav-link[data-target="${activeSec}"]`);
      if (activeLink && navIndicator) {
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        activeLink.classList.add('active');
        navIndicator.style.left = `${activeLink.offsetLeft}px`;
        navIndicator.style.width = `${activeLink.offsetWidth}px`;
      }

      // Also update mobile nav pill active link
      document.querySelectorAll('#navPillMobile .nav-link').forEach(l => {
        l.classList.toggle('active', l.dataset.target === activeSec);
      });

      if (activeSec === 'shop') {
        nav.classList.add('light');
      } else {
        nav.classList.remove('light');
      }
    }

    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.dataset.target;
        document.getElementById(targetId).scrollIntoView({ behavior: 'smooth' });
      });
    });

    requestAnimationFrame(render);

  </script>
</body>
</html>
'''

with open(os.path.join('public', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Updated public/index.html with high-contrast buttons, responsive layout, and WhatsApp integration successfully!")
