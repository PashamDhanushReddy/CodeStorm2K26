document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById('code-canvas');
    if (!canvas) return;

    // SCROLLING CODE SETUP
    const ctx = canvas.getContext('2d');
    canvas.width = 1024;
    canvas.height = 768;

    let codeOffsetY = 768;
    const codeLines = [
        "CodeStorm-2K26",
        "",
        "const hackathon = {",
        "  event: 'CodeStorm 2K26',",
        "  duration: '36 Hours',",
        "  creativity: true,",
        "  innovation: '∞',",
        "  status: 'Registration Open'",
        "};",
        "",
        "async function buildFuture() {",
        "  console.log('Ideate. Build. Deploy.');",
        "  return await Hackathon.launch('CodeStorm');",
        "}",
        "",
        "// --------------------------------",
        "// Initialize main systems...",
        "// --------------------------------",
        "hackathon.start();",
        "",
        "if (user.hasIdea) {",
        "  execute(user.idea);",
        "  winPrize('₹2,00,000');",
        "}",
        "",
        "function getReady() {",
        "  const coffee = true;",
        "  const sleep = false;",
        "  return coffee && !sleep;",
        "}"
    ];

    function drawScreen() {
        ctx.fillStyle = '#0f172a'; // Dark IDE background
        ctx.fillRect(0, 0, 1024, 768);

        // IDE Top Bar
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(0, 0, 1024, 50);
        
        ctx.fillStyle = '#94a3b8';
        ctx.font = '24px "Orbitron", sans-serif';
        ctx.fillText('main.js — CodeStorm IDE', 20, 34);
        
        // Window controls
        ctx.fillStyle = '#ef4444'; ctx.beginPath(); ctx.arc(940, 25, 8, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#eab308'; ctx.beginPath(); ctx.arc(970, 25, 8, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#22c55e'; ctx.beginPath(); ctx.arc(1000, 25, 8, 0, Math.PI*2); ctx.fill();

        // Draw code
        ctx.font = '28px monospace';
        const lineHeight = 40;
        
        for (let i = 0; i < codeLines.length; i++) {
            const line = codeLines[i];
            const y = codeOffsetY + (i * lineHeight);
            
            if (line.includes('CodeStorm-2K26') && !line.includes('return') && !line.includes('event')) {
                ctx.fillStyle = '#6366f1'; 
                ctx.font = 'bold 36px "Orbitron", sans-serif';
            } else if (line.startsWith('const') || line.startsWith('function') || line.startsWith('async') || line.includes('await') || line.startsWith('if') || line.startsWith('return')) {
                ctx.fillStyle = '#f43f5e'; 
                ctx.font = 'bold 28px monospace';
            } else if (line.includes("'") || line.includes('"')) {
                ctx.fillStyle = '#10b981'; 
                ctx.font = '28px monospace';
            } else if (line.startsWith('//')) {
                ctx.fillStyle = '#64748b'; 
                ctx.font = 'italic 28px monospace';
            } else if (line.includes('true') || line.includes('false')) {
                ctx.fillStyle = '#eab308'; 
                ctx.font = 'bold 28px monospace';
            } else {
                ctx.fillStyle = '#f8fafc'; 
                ctx.font = '28px monospace';
            }
            
            // Wrap around logic
            let drawY = y;
            while(drawY < 50) drawY += (codeLines.length * lineHeight);
            while(drawY > 768 + (codeLines.length * lineHeight)) drawY -= (codeLines.length * lineHeight);
            
            if (drawY > 50 && drawY < 800) {
                ctx.fillText(line, 30, drawY);
            }
        }
        
        // Scroll speed
        codeOffsetY -= 3.5;
        if (codeOffsetY < -(codeLines.length * lineHeight)) {
            codeOffsetY = 768;
        }
    }

    // ==========================================
    // PARALLAX & BADGE ANIMATION
    // ==========================================
    const coderGroup = document.getElementById('coder-group');
    const badges = document.querySelectorAll('.badge');
    
    let mouseX = 0;
    let mouseY = 0;
    let currentX = 0;
    let currentY = 0;
    
    document.addEventListener('mousemove', (e) => {
        // Normalize -1 to 1
        mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    });

    let scrollY = 0;
    let currentScroll = 0;
    document.addEventListener('scroll', () => {
        scrollY = window.scrollY;
    });

    function animate() {
        requestAnimationFrame(animate);
        
        // 1. Draw Canvas
        drawScreen();

        // 2. Parallax Lerp (JS handles smooth mouse parallax)
        currentX += (mouseX * 15 - currentX) * 0.1;
        currentY += (mouseY * -15 - currentY) * 0.1;
        
        // Scroll translation (push up and away as user scrolls)
        currentScroll += (scrollY - currentScroll) * 0.1;
        const scrollOffset = currentScroll * 0.45;

        // Apply to Coder Group
        if (coderGroup) {
            coderGroup.style.transform = `
                translate3d(${currentX}px, ${currentY + scrollOffset}px, 0)
                rotateX(${currentY * 0.08}deg)
                rotateY(${currentX * 0.08}deg)
            `;
        }
    }

    animate();
});
