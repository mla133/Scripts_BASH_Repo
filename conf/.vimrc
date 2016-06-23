set nocompatible
filetype plugin on
set term=ansi
set title
set number	" show line numbers
set cursorline 	" highlight current line
set showmatch	" highlight matching [{()}]
set foldenable  " enable folding
set foldlevelstart=0 	" open most folds by default
set foldnestmax=10	" 10 nested fold max setting
set laststatus=2	" Always show status line
set statusline=\ %{HasPaste()}%F%m%r%h\ %w\ \ CMD:\ %r{getcd()}%h\ \ \ Line:\ %l
set nobackup
set noswapfile


syntax on
hi Comment term=none ctermfg=green ctermbg=darkgray guifg=Gray
se hlsearch
" Ctrl-L clears the highlight from the last search
noremap <C-l> :nohlsearch<CR><C-l>
noremap! <C-l> <ESC>:nohlsearch<CR><C-l>
autocmd! BufNewFile,BufRead *.ino setlocal ft=arduino

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Helper functions
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! CmdLine(str)
	exe "menu Foo.Bar :" . a:str
        emenu Foo.Bar
        unmenu Foo
endfunction

function! VisualSelection(direction) range
        let l:saved_reg = @"
        execute "normal! vgvy"

        let l:pattern = escape(@", '\\/.*$^~[]')
        let l:pattern = substitute(l:pattern, "\n$", "", "")

    if a:direction == 'b'
        execute "normal ?" . l:pattern . "^M"
    elseif a:direction == 'gv'
        call CmdLine("vimgrep " . '/'. l:pattern . '/' . ' **/*.')
    elseif a:direction == 'replace'
        call CmdLine("%s" . '/'. l:pattern . '/')
    elseif a:direction == 'f'
        execute "normal /" . l:pattern . "^M"
    endif

    let @/ = l:pattern
    let @" = l:saved_reg
endfunction


" Returns true if paste mode is enabled
function! HasPaste()
    if &paste
        return 'PASTE MODE  '
    en
        return ''
endfunction

" Don't close window, when deleting a buffer
command! Bclose call <SID>BufcloseCloseIt()

function! <SID>BufcloseCloseIt()
    let l:currentBufNum = bufnr("%")
    let l:alternateBufNum = bufnr("#")

    if buflisted(l:alternateBufNum)
        buffer #
    else
        bnext
    endif

    if bufnr("%") ==
        l:currentBufNum
        new
    endif

    if
        buflisted(l:currentBufNum)
        execute("bdelete! ".l:currentBufNum)
    endif
endfunction
