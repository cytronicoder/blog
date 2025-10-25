#!/usr/bin/env node
/**
 * Generate cover images for all blog posts
 * This can be run during the build process
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const POSTS_DIR = path.join(__dirname, '../posts');
const PUBLIC_DIR = path.join(__dirname, '../public/covers');
const SCRIPT_PATH = path.join(__dirname, 'generate-cover.py');

if (!fs.existsSync(PUBLIC_DIR)) {
    fs.mkdirSync(PUBLIC_DIR, { recursive: true });
}

if (!fs.existsSync(SCRIPT_PATH)) {
    console.error('Error: generate-cover.py not found');
    process.exit(1);
}

const posts = fs.readdirSync(POSTS_DIR)
    .filter(file => file.endsWith('.md'));

console.log(`Found ${posts.length} blog posts\n`);

let generated = 0;
let skipped = 0;

posts.forEach(postFile => {
    const slug = path.basename(postFile, '.md');
    const postPath = path.join(POSTS_DIR, postFile);
    const outputPath = path.join(PUBLIC_DIR, `${slug}.png`);

    const content = fs.readFileSync(postPath, 'utf8');
    const { data } = matter(content);

    if (data.image && data.image.startsWith('http')) {
        console.log(`⊘ Skipping ${slug} (manual image set)`);
        skipped++;
        return;
    }

    if (fs.existsSync(outputPath) && !process.argv.includes('--force')) {
        console.log(`⊘ Skipping ${slug} (image exists, use --force to regenerate)`);
        skipped++;
        return;
    }

    try {
        console.log(`Generating cover for: ${slug}`);
        execSync(
            `python3 "${SCRIPT_PATH}" "${postPath}" -o "${outputPath}"`,
            { stdio: 'inherit' }
        );

        const newData = {
            ...data,
            image: `/covers/${slug}.png`
        };

        const newContent = matter.stringify(content.split('---').slice(2).join('---').trim(), newData);
        fs.writeFileSync(postPath, newContent);

        console.log(`✓ Updated ${slug} frontmatter\n`);
        generated++;

    } catch (error) {
        console.error(`✗ Error generating cover for ${slug}:`, error.message);
    }
});

console.log(`\n${'='.repeat(50)}`);
console.log(`Generated: ${generated} | Skipped: ${skipped} | Total: ${posts.length}`);
console.log(`${'='.repeat(50)}\n`);
