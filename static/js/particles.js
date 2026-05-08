// RavenBuilds ember particle network
(function(){
  const canvas = document.getElementById('particles');
  const ctx    = canvas.getContext('2d');
  let W, H, particles = [], mouse = {x:-1000,y:-1000};

  const N    = 55;
  const DIST = 120;
  const COLOR = '255,120,0';

  function resize(){
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function Particle(){
    this.x  = Math.random() * W;
    this.y  = Math.random() * H;
    this.vx = (Math.random() - 0.5) * 0.35;
    this.vy = (Math.random() - 0.5) * 0.35 - 0.1; // slight upward drift like embers
    this.r  = Math.random() * 1.4 + 0.5;
    this.flicker = Math.random() * Math.PI * 2;
  }

  function init(){
    resize();
    particles = Array.from({length:N},()=>new Particle());
  }

  function draw(){
    ctx.clearRect(0,0,W,H);

    // move
    particles.forEach(p=>{
      p.x += p.vx; p.y += p.vy;
      p.flicker += 0.05;
      if(p.x<0||p.x>W) p.vx*=-1;
      if(p.y<0) p.y=H;
      if(p.y>H) p.y=0;
    });

    // connect
    for(let i=0;i<particles.length;i++){
      for(let j=i+1;j<particles.length;j++){
        const a=particles[i], b=particles[j];
        const dx=a.x-b.x, dy=a.y-b.y;
        const d=Math.sqrt(dx*dx+dy*dy);
        if(d<DIST){
          const op = (1-d/DIST)*0.18;
          ctx.beginPath();
          ctx.strokeStyle=`rgba(${COLOR},${op})`;
          ctx.lineWidth=0.5;
          ctx.moveTo(a.x,a.y);
          ctx.lineTo(b.x,b.y);
          ctx.stroke();
        }
      }
      // mouse interact
      const dx=particles[i].x-mouse.x, dy=particles[i].y-mouse.y;
      const d=Math.sqrt(dx*dx+dy*dy);
      if(d<200){
        const op=(1-d/200)*0.45;
        ctx.beginPath();
        ctx.strokeStyle=`rgba(255,180,0,${op})`;
        ctx.lineWidth=0.7;
        ctx.moveTo(particles[i].x,particles[i].y);
        ctx.lineTo(mouse.x,mouse.y);
        ctx.stroke();
      }
    }

    // draw ember dots
    particles.forEach(p=>{
      const flick = 0.4 + Math.sin(p.flicker) * 0.2;
      ctx.beginPath();
      ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(${COLOR},${flick})`;
      ctx.fill();
    });

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize',resize);
  document.addEventListener('mousemove',e=>{mouse.x=e.clientX;mouse.y=e.clientY});
  document.addEventListener('mouseleave',()=>{mouse.x=-1000;mouse.y=-1000});

  init();
  draw();
})();
