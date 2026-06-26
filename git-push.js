const { execSync } = require('child_process')
const cwd = 'D:\\personal\\project\\admin-web'

function run(cmd) {
  console.log('> ' + cmd)
  try {
    const output = execSync(cmd, { cwd, encoding: 'utf8', stdio: 'pipe' })
    console.log(output || '(no output)')
  } catch (e) {
    console.error('ERROR:', e.message)
    if (e.stdout) console.log('STDOUT:', e.stdout.toString())
    if (e.stderr) console.error('STDERR:', e.stderr.toString())
    process.exit(1)
  }
}

console.log('Current branch:')
run('git branch --show-current')

console.log('\nGit status:')
run('git status --short')

console.log('\nStaging changes...')
run('git add .')

console.log('\nCommitting...')
run('git commit -m "feat: 大屏菜单分组与5套行业数据可视化大屏"')

console.log('\nPushing to origin main...')
run('git push -u origin main')

console.log('\nDone.')
