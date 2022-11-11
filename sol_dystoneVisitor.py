from gen.SolidityVisitor import SolidityVisitor
from gen.SolidityParser import SolidityParser

class sol_dystoneVisitor(SolidityVisitor):

    def __init__(self):
        self.rindex = {}#키: 변수이름, 값:self.count 인덱스 # 0:me 1:me/all
        self.tlist = []#같은의미를 나타내는 tuple list
        self.stlist =[]#같은 의미를 나타내는 string tuple list ex) me, hospital과 같은 인자 저장
        self.parent = []#constraint 정보 배열

        self.cname =[]#전역 변수 인덱싱한 name
        self.name =[] #로컬 변수 인덱싱한 name

        self.isUse = False #reveal 사용 유무 체크
        self.isMapping = []#mapping인 변수

        self.fcnt = 1 #함수 인덱스 카운트
        self.count =1 #변수 인덱스 카운트

    #union find - optimizer를 위한 것
    def find_parent(self, parent, x):
        if parent[x] != x:
            return self.find_parent(parent, parent[x])
        return parent[x]

    def union_parent(self, parent, a, b):
        a = self.find_parent(parent, a)
        b = self.find_parent(parent, b)
        if a < b:
            parent[b] = a
        else:
            parent[a] = b

    # Visit a parse tree produced by SolidityParser#sourceUnit.
    def visitSourceUnit(self, ctx:SolidityParser.SourceUnitContext):
        cd1 = ""
        for i in range (1,ctx.getChildCount()-1):
            cd1 += self.visitContractDefinition(ctx.getChild(i))
        str1 = self.visitPragmaDirective(ctx.getChild(0)) + cd1

        self.tlist.sort(key=lambda x:x[0]) # tuplelist 첫번째 원소를 기준으로 정렬
        print("변수 관계 오름차순 정리 결과 :",end=" ")
        print(self.tlist)
        print("문자열로 이루어진 변수 관계 결과 :",end=" ")
        print(self.stlist)
        # tlist 로 parent 값 넣기
        self.parent = [i for i in range(0, self.count + 1)]
        for i in self.tlist:
            if isinstance(i[0], int) and isinstance(i[1], int):
                self.union_parent(self.parent, i[0], i[1])


        print("union-find 결과 :",end=" ")
        print(self.parent)
        print()
        #초기화
        self.rindex = {}
        self.tlist =[]
        self.stlist =[]

        self.cname = []
        self.name = []

        self.isUse = False
        self.isMapping =[]

        self.fcnt = 1
        self.count =1

        cd2 = ""
        #parent 정보를 이용해 optimizer
        for i in range (1,ctx.getChildCount()-1):
            cd2 += self.visitContractDefinition(ctx.getChild(i))
        str2 = self.visitPragmaDirective(ctx.getChild(0)) + cd2

        #optimize 전과 후 동시 출력
        str = str1 +"\n"+ str2

        with open("../Dystonizer/output/dystone_Output.stn", "w") as text_file:
            text_file.write(str)
        print("Dystonizer done")
        return str


    # Visit a parse tree produced by SolidityParser#pragmaDirective.
    def visitPragmaDirective(self, ctx:SolidityParser.PragmaDirectiveContext):
        str = ctx.getChild(0).__str__()+" "+ self.visitVersionPragma(ctx.pragma())+ctx.getChild(2).__str__()+"\n\n"
        return str


    # Visit a parse tree produced by SolidityParser#VersionPragma.
    def visitVersionPragma(self, ctx:SolidityParser.VersionPragmaContext):
        str = ctx.getChild(0).__str__()+" "+self.visitVersion(ctx.version())
        return str


    # Visit a parse tree produced by SolidityParser#version.
    def visitVersion(self, ctx:SolidityParser.VersionContext):
        #versionConstraint versionConstraint?
        str= self.visitVersionConstraint(ctx.versionConstraint(0))
        if ctx.getChildCount()>1:
            str+= self.visitVersionConstraint(ctx.versionConstraint(1))
        return str

    # Visit a parse tree produced by SolidityParser#versionOperator.
    def visitVersionOperator(self, ctx:SolidityParser.VersionOperatorContext):
        #  '^' | '~' | '>=' | '>' | '<' | '<=' | '='
        str = ctx.getChild(0).__str__()
        return str

    # Visit a parse tree produced by SolidityParser#versionConstraint.
    def visitVersionConstraint(self, ctx:SolidityParser.VersionConstraintContext):
        # versionOperator VersionLiteral
        if ctx.getChildCount() > 1:
            str = self.visitVersionOperator(ctx.versionOperator())+ ctx.getChild(1).__str__()
        #  VersionLiteral
        else:
            str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#contractDefinition.
    def visitContractDefinition(self, ctx:SolidityParser.ContractDefinitionContext):
        cp = ""
        str = ctx.getChild(0).__str__()+ " "+self.visitIdentifier(ctx.identifier())+" "+ctx.getChild(2).__str__()+"\n"
        for i in range (0, ctx.getChildCount()-4):
            cp += "    "+self.visitContractPart(ctx.contractPart(i)) + '\n'
        str += cp + ctx.getChild(ctx.getChildCount()-1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#contractPart.
    def visitContractPart(self, ctx:SolidityParser.ContractPartContext):
        res = '\n\t' if ctx.constructorDefinition() else ''
        res += self.visit(ctx.getChild(0))
        # 아래로 내려가기만 함
        return res


    # Visit a parse tree produced by SolidityParser#stateVariableDeclaration.
    def visitStateVariableDeclaration(self, ctx:SolidityParser.StateVariableDeclarationContext):
        # ( keywords+=FinalKeyword )* annotated_type=annotatedTypeName
        # ( keywords+=ConstantKeyword )*
        # idf=identifier ('=' expr=expression)? ';'

        res=""
        anotindex = 0
        idfindex = 0

        at = ctx.annotatedTypeName()
        id = ctx.identifier()
        it = self.visitIdentifier(id)
        for i in range(0, ctx.getChildCount()):
            if at is ctx.getChild(i):
                anotindex = i
            elif id is ctx.getChild(i):
                idfindex = i

        for i in range(0, anotindex):
            res += ctx.getChild(i).__str__()+" "

        vat = self.visitAnnotatedTypeName(at)
        # 변수 타입이 address가 아니면 변수에 @태그 추가
        if vat != "address":
            isparent = False
            #parent가 업데이트 됐는지 확인
            if len(self.parent) != 0:
               isparent = True
            # parent를 업데이트한 상태이면, parent의 값 사용
            if isparent:
                res += vat+"@_t"+str(self.parent[self.count])+" "
            else:
                res += vat+"@_t"+str(self.count)+" "
            self.cname.append(it) #전역 변수 이름 추가

            #mapping이 아닌경우 인덱싱 정보 추가
            if "mapping" not in vat:
                self.rindex[it] = self.count
            self.count += 1
        else:
            res += vat+" "
            self.count += 1

        for i in range(anotindex+1, idfindex):
            res += ctx.getChild(i).__str__()

        #identifier 추가
        res += it

        if ctx.identifier() is ctx.getChild(ctx.getChildCount()-2):
            res += ctx.getChild(ctx.getChildCount()-1).__str__()
        else:
            res += ctx.getChild(ctx.getChildCount()-3).__str__()+ctx.visit(ctx.expression())+ctx.getChild(ctx.getChildCount()-1).__str__()

        return res


    # Visit a parse tree produced by SolidityParser#constructorDefinition.
    def visitConstructorDefinition(self, ctx:SolidityParser.ConstructorDefinitionContext):
        #함수마다 @태그 추가, constructor도 포함
        res = "@c"+str(self.fcnt)+"\n\t"
        self.fcnt += 1
        res += ctx.getChild(0).__str__() + self.visitParameterList(ctx.parameterList()) + self.visitModifierList(ctx.modifierList())+ self.visitBlock(ctx.block())
        return res

    # Visit a parse tree produced by SolidityParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:SolidityParser.FunctionDefinitionContext):
        #'function' idf=identifier parameters=parameterList modifiers=modifierList return_parameters=returnParameters? body=block

        #'태깅된 변수의 이름이담긴 배열(name)'이 비어있지 않는 경우,
        #해당 배열을 읽으면서 '인덱스 사이 관계 정보가 담긴(ridedx)' 정보도 삭제
        if len(self.name) !=0:
            for i in self.name:
                if i in self.rindex:
                    self.rindex.pop(i)
            self.name = []

        #다음 함수를 읽을때도 인덱스 정보가 연결되야하므로, 임시 저장
        temp = self.count
        res = ""
        tagflag = False

        #해당 클래스 인덱스 정보에 해당하는 정보(stlist)가 있으면, 클래스 태그 이름 변경하기
        if len(self.parent) != 0:
            for i in self.stlist:
                if self.fcnt == i[1]:
                    res = '@'+i[0]+"\n    "
                else:
                    tagflag = True
        else:
            tagflag = True
        #(0) @c_k 를 붙인다 (k는 새로운 숫자)
        if tagflag:
            res ='@c'+str(self.fcnt)+"\n    "
        res += ctx.getChild(0).__str__()+" "+ self.visitIdentifier(ctx.identifier())
        tpar = self.visitParameterList(ctx.parameterList())+self.visitModifierList(ctx.modifierList())

        if ctx.getChildCount()>5:#return문 있는경우
            wplist = " "+self.visitReturnParameters(ctx.returnParameters())+ self.visitBlock(ctx.block())
        else:#return 문 없는 경우
            wplist = self.visitBlock(ctx.block())
        #(4) (2)-(3)에 _reveal을 모두 확인해서, 형식인자에 ">"를 삽입한다.
        if '_reveal' in wplist: #reveal이 사용된 경우 다시한번 파싱
            # 파라미터 추가
            # 초기화 먼저하기
            self.count = temp
            self.name = []
            res += self.visitParameterList(ctx.parameterList())+self.visitModifierList(ctx.modifierList())
            if ctx.getChildCount() > 5:
                res += " "+self.visitReturnParameters(ctx.returnParameters()) + self.visitBlock(ctx.block())
            else:
                res += self.visitBlock(ctx.block())
        else:#사용되지 않은경우 기존 내용 더해주기
            res += tpar + wplist

        self.fcnt += 1 #fluction 개수 카운팅
        self.isUse = False #하나의 function 탐색후 초기화
        return res

    # Visit a parse tree produced by SolidityParser#returnParameters.
    def visitReturnParameters(self, ctx:SolidityParser.ReturnParametersContext):
        str = ctx.getChild(0).__str__() +" " + self.visitParameterList(ctx.parameterList())
        return str

    # Visit a parse tree produced by SolidityParser#modifierList.
    def visitModifierList(self, ctx:SolidityParser.ModifierListContext):
        str = ""
        if ctx.getChildCount()>0:
            for i in range (0, ctx.getChildCount()):
                str +=' '+ self.visitModifier(ctx.modifier(i))
        return str


    # Visit a parse tree produced by SolidityParser#modifier.
    def visitModifier(self, ctx:SolidityParser.ModifierContext):
        #바로 아래로 내려보내기
        if ctx.getChild(0).__str__().__eq__('public') or ctx.getChild(0).__str__().__eq__("internal") or ctx.getChild(0).__str__().__eq__("private"):
            return ctx.getChild(0).__str__()
        else:
            return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#parameterList.
    def visitParameterList(self, ctx:SolidityParser.ParameterListContext):
        res = ctx.getChild(0).__str__()
        #'(' ( params+=parameter (',' params+=parameter)* ) ')'
        if ctx.getChildCount()>2:
            res += self.visitParameter(ctx.parameter(0))
            pr = ""
            for i in range (2, ctx.getChildCount()-1,2):
                pr+= ctx.getChild(i).__str__()+" "+ self.visitParameter(ctx.getChild(i+1))
            res += pr
        # '(' ')'
        res += ctx.getChild(ctx.getChildCount()-1).__str__()
        return res


    # Visit a parse tree produced by SolidityParser#parameter.
    #(keywords+=FinalKeyword)? annotated_type=annotatedTypeName idf=identifier? ;
    def visitParameter(self, ctx:SolidityParser.ParameterContext):
        res = ""
        index=0
        for i in range(0, ctx.getChildCount()):# annotated_type 기준으로 나머지 index 추론
            if ctx.annotatedTypeName() is ctx.getChild(i):
                index = i
                break

        #FinalKeyword 추가
        for i in range(0, index):
            res += ctx.getChild(i).__str__()+" "

        #annotated_type 추가
        mytype = self.visitAnnotatedTypeName(ctx.annotatedTypeName())

        myid = ""
        #identifier있으면 추가
        if(index != ctx.getChildCount()-1):
            myid = self.visitIdentifier(ctx.identifier())

        if ctx.getChild(0) is ctx.annotatedTypeName():#formal parameter 중
            #(1) formal parameter 중 Address가 아닌 타입에 대해서는 @_t_i 를 붙인다. (i는 새로운 숫자)
            if mytype != "address":
                #@_ti를 붙인다 , i는 인덱스

                #parent 업데이트 유무 확인
                isparent = False
                if len(self.parent) !=0:
                    isparent = True

                if self.isUse: #reveal 대상이 있으면 '>' 추가
                    if isparent:#parent정보가 있는 경우
                        pc = self.parent[self.count]
                        if pc == 0 or pc == 1: #me/all인 경우 원래 인덱스 사용
                            res = mytype +"@_t"+str(self.count)+">@_t"
                        else:
                            res = mytype +"@_t"+str(self.parent[self.count])+">@_t"
                        #중복 원소 처리
                        if (1,self.count) not in self.tlist:
                            self.tlist.append((1,self.count))

                        self.count += 1

                        pc=self.parent[self.count]
                        if pc ==0 or pc == 1: #me/all인 경우 원래 인덱스 사용
                            res += str(self.count)+" "+myid
                        else:
                            res += str(self.parent[self.count])+" "+myid
                    else:#parent정보가 없는 경우
                        res = mytype +"@_t"+str(self.count)+">@_t"
                        #중복 원소 처리
                        if (1,self.count) not in self.tlist:
                            self.tlist.append((1,self.count))

                        self.count += 1

                        res += str(self.count)+" "+myid

                        self.rindex[myid] = self.count # reveal target index 저장, 함수 내부에서 사용
                else:#reveal이 사용되지 않으면 '>' 추가하지 않음
                    if isparent:
                        res =mytype+"@_t"+str(self.parent[self.count])+" "+myid
                    else:
                        res =mytype+"@_t"+str(self.count)+" "+myid

                self.name.append(myid)#이름을 로컬 변수 베열에 추가
                self.count += 1 #인덱스 증가
            else:
                res =mytype+" "+myid
        return res

    # Visit a parse tree produced by SolidityParser#enumValue.
    # idf=identifier
    def visitEnumValue(self, ctx:SolidityParser.EnumValueContext):
        str = self.visitIdentifier(ctx.identifier())
        return str


    # Visit a parse tree produced by SolidityParser#enumDefinition.
    def visitEnumDefinition(self, ctx:SolidityParser.EnumDefinitionContext):
        #'enum' idf=identifier '{' values+=enumValue? (',' values+=enumValue)* '}'
        str = ctx.getChild(0).__str__() + " " + self.visitIdentifier(ctx.identifier()) + " " + ctx.getChild(2).__str__()+" "

        if ctx.getChildCount()>4:
            if ctx.enumValue(0) is ctx.getChild(ctx.getChildCount()-2):
                str += self.visitEnumValue(ctx.enumValue(0))
            else:
                str += self.visitEnumValue(ctx.enumValue(0))
                ev = ""
                for i in range (4, ctx.getChildCount()-1, 2):
                    ev += ctx.getChild(i).__str__() +" "+ self.visitEnumValue(ctx.getChild(i+1))
                str += ev+ " "
        str += " "+ctx.getChild(ctx.getChildCount()-1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:SolidityParser.VariableDeclarationContext):
        #function vars json 가져오기
        # (keywords+=FinalKeyword) annotated_type=annotatedTypeName idf=identifier
        res = ""
        if ctx.getChild(0) != ctx.annotatedTypeName():
            res += ctx.getChild(0).__str__() + " "
        res += self.visitAnnotatedTypeName(ctx.annotatedTypeName())+" "+self.visitIdentifier(ctx.identifier())
        return res

    # Visit a parse tree produced by SolidityParser#typeName.
    def visitTypeName(self, ctx:SolidityParser.TypeNameContext):
        #바로 아래로 보내기
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#userDefinedTypeName.
    def visitUserDefinedTypeName(self, ctx:SolidityParser.UserDefinedTypeNameContext):
        #names+=identifier ( '.' names+=identifier )*
        res = self.visitIdentifier(ctx.identifier(0))
        dt = ""
        for i in range(1, ctx.getChildCount(), 2):
            dt += ctx.getChild(i)+self.visitIdentifier(ctx.getChild(i+1))
        res += dt
        return res


    # Visit a parse tree produced by SolidityParser#mapping.
    def visitMapping(self, ctx:SolidityParser.MappingContext):
        #'mapping' '(' key_type=elementaryTypeName ( '!' key_label=identifier )? '=>' value_type=annotatedTypeName ')'
        #부모트리로 부터 mapping의 이름 정보 가져오기
        name = ctx.parentCtx.parentCtx.parentCtx.getChild(1).getChild(0).__str__()
        #mapping이므로 리스트에 추가
        self.isMapping.append(name)

        etindex =0
        atindex =0
        res = ctx.getChild(0).__str__()+ctx.getChild(1).__str__()

        for i in range(ctx.getChildCount()):
            if ctx.elementaryTypeName() is ctx.getChild(i):
                etindex = i
            elif ctx.annotatedTypeName() is ctx.getChild(i):
                atindex = i

        #elementaryTypeName 추가
        res += self.visitElementaryTypeName(ctx.elementaryTypeName())

        if (atindex - etindex) != 2:
            res += ctx.getChild(3).__str__()+self.visitIdentifier(ctx.identifier())
        #parent 배열 업데이트 유무 확인
        isparent = False
        if len(self.parent)!=0:
            isparent =True

        if isparent:#parent가 업데이트 된경우 사용
            res += "!_t"+str(self.parent[self.count])
            self.count += 1
            res += ctx.getChild(atindex-1).__str__()+" "+self.visitAnnotatedTypeName(ctx.annotatedTypeName())+"@_t"+str(self.parent[self.count])
            #인덱스 정보 추가하기
            self.rindex[name] = self.count
        else:
            res +="!_t"+str(self.count)
            self.count += 1
            res += ctx.getChild(atindex-1).__str__()+" "+self.visitAnnotatedTypeName(ctx.annotatedTypeName())+"@_t"+str(self.count)
            #인덱스 정보 추가하기
            self.rindex[name] = self.count
        self.count += 1
        res += ctx.getChild(ctx.getChildCount()-1).__str__()
        return res

    # Visit a parse tree produced by SolidityParser#stateMutability.
    def visitStateMutability(self, ctx:SolidityParser.StateMutabilityContext):
        #문자열 출력하기
        str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#block.
    def visitBlock(self, ctx:SolidityParser.BlockContext):
        # '{' statements+=statement* '}'
        st = ""
        sp = "" #들여쓰기를 의한것
        sp2 = "    " # statement 들여쓰기를 위한것
        i= int(len(ctx.parentCtx.__str__()) / 12)
        for i in range(0,i):
            sp+="    "

        str = " "+ctx.getChild(0).__str__() +"\n"
        for i in range (1, ctx.getChildCount()-1):
            st += sp+sp2+self.visitStatement(ctx.getChild(i))+"\n"
        str += st+ sp+ctx.getChild(ctx.getChildCount()-1).__str__()+"\n"
        return str


    # Visit a parse tree produced by SolidityParser#statement.
    def visitStatement(self, ctx:SolidityParser.StatementContext):
        #바로 아래로 내려보내기
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#expressionStatement.
    def visitExpressionStatement(self, ctx:SolidityParser.ExpressionStatementContext):
        #expr=expression ';'
        str = self.visit(ctx.expression()) + ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#ifStatement.
    def visitIfStatement(self, ctx:SolidityParser.IfStatementContext):
        #'if' '(' condition=expression ')' then_branch=statement
        str = ctx.getChild(0).__str__() +ctx.getChild(1).__str__()+ self.visit(ctx.expression())+ctx.getChild(3).__str__()+ self.visitStatement(ctx.statement(0))+"     "
        if ctx.getChildCount()>6:
            #'if' '(' condition=expression ')' then_branch=statement ( 'else' else_branch=statement )
            str += "    "+ctx.getChild(5).__str__()+self.visitStatement(ctx.statement(1))
        return str


    # Visit a parse tree produced by SolidityParser#whileStatement.
    def visitWhileStatement(self, ctx:SolidityParser.WhileStatementContext):
        #'while' '(' condition=expression ')' body=statement ;
        str = ctx.getChild(0).__str__()+" " +ctx.getChild(1).__str__() +self.visit(ctx.expression())+ctx.getChild(3).__str__()+ self.visitStatement(ctx.statement())
        return str


    # Visit a parse tree produced by SolidityParser#simpleStatement.
    def visitSimpleStatement(self, ctx:SolidityParser.SimpleStatementContext):
        #아래로 바로 보내기
        # ( variableDeclarationStatement | expressionStatement )
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#forStatement.
    def visitForStatement(self, ctx:SolidityParser.ForStatementContext):
        #  원본 'for' '(' ( init=simpleStatement | ';' ) condition=expression? ';' update=expression? ')' body=statement
        str = ctx.getChild(0).__str__()+" "+ctx.getChild(1).__str__()
        #'for' '(' ( ';' )
        if ctx.getChild(2).__str__().__eq__(";"):
            str+= ctx.getChild(2).__str__()
        #'for' '(' (init=simpleStatement)
        else:
            str+= self.visitSimpleStatement(ctx.simpleStatement())

        # condition=expression ';' update=expression ')' body=statement
        if ctx.getChildCount()>7:
            str+= " "+self.visit(ctx.expression(0))+ctx.getChild(4).__str__()+" "+ self.visit(ctx.expression(1))
        elif ctx.getChildCount()>6:
            #  ';' update=expression ')' body=statement
            if ctx.getChild(3).__str__().__eq__(";"):
                str+= ctx.getChild(3).__str__()+" "+ self.visit(ctx.getChild(4))
            # condition=expression ';'  ')' body=statement
            else:
                str+= " " +self.visit(ctx.getChild(3))+ctx.getChild(4).__str__()+" "
        # ';' ')' body=statement
        else:
            str += ctx.getChild(3).__str__()
        str += ctx.getChild(ctx.getChildCount()-2).__str__() + self.visitStatement(ctx.statement())
        return str


    # Visit a parse tree produced by SolidityParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:SolidityParser.DoWhileStatementContext):
        str = ctx.getChild(0).__str__()+self.visitStatement(ctx.statement())+"    "+ ctx.getChild(2).__str__() +ctx.getChild(3).__str__() + self.visit(ctx.expression())+ctx.getChild(5).__str__()+ctx.getChild(6).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#continueStatement.
    def visitContinueStatement(self, ctx:SolidityParser.ContinueStatementContext):
        str = ctx.getChild(0).__str__()+ctx.getChild(1).__str__()
        return str

    # Visit a parse tree produced by SolidityParser#breakStatement.
    def visitBreakStatement(self, ctx:SolidityParser.BreakStatementContext):
        str = ctx.getChild(0).__str__()+ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#returnStatement.
    def visitReturnStatement(self, ctx:SolidityParser.ReturnStatementContext):
        if ctx.getChildCount()>2:
            #return expression ;
            str = ctx.getChild(0).__str__() +" "+self.visit(ctx.expression())+ctx.getChild(2).__str__()
        else:
            #return ;
            str = ctx.getChild(0).__str__()+ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#variableDeclarationStatement.
    def visitVariableDeclarationStatement(self, ctx:SolidityParser.VariableDeclarationStatementContext):
        str = self.visitVariableDeclaration(ctx.variableDeclaration())
        if ctx.getChildCount()>2:
            # variable_declaration=variableDeclaration ( '=' expr=expression ) ';'
            str += " "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression())+ctx.getChild(3).__str__()
        else:
            # variable_declaration=variableDeclaration ';'
            str +=  ctx.getChild(1).__str__()

        return str


    # Visit a parse tree produced by SolidityParser#elementaryTypeName.
    def visitElementaryTypeName(self, ctx:SolidityParser.ElementaryTypeNameContext):
        str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#AndExpr.
    def visitAndExpr(self, ctx:SolidityParser.AndExprContext):
        # lhs=expression op='&&' rhs=expression
        str = self.visit(ctx.expression(0)) +" "+ ctx.getChild(1).__str__() +" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#ParenthesisExpr.
    def visitParenthesisExpr(self, ctx:SolidityParser.ParenthesisExprContext):
        #'(' expr=expression ')'
        str = ctx.getChild(0).__str__()+ self.visit(ctx.expression())+ ctx.getChild(2).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#BitwiseOrExpr.
    def visitBitwiseOrExpr(self, ctx:SolidityParser.BitwiseOrExprContext):
        #lhs=expression op='|' rhs=expression
        str =self.visit(ctx.expression(0)) + ctx.getChild(1).__str__() + self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#AllExpr.
    def visitAllExpr(self, ctx:SolidityParser.AllExprContext):
        #AllKeyword
        str= ctx.getChild(0).__str__()
        return str

    # Visit a parse tree produced by SolidityParser#IteExpr.
    def visitIteExpr(self, ctx:SolidityParser.IteExprContext):
        #cond=expression '?' then_expr=expression ':' else_expr=expression
        str = self.visit(ctx.expression(0))+" " +ctx.getChild(1).__str__()+" " +self.visit(ctx.expression(1))+" "+ ctx.getChild(3).__str__()+" "+self.visit(ctx.expression(2))
        return str


    # Visit a parse tree produced by SolidityParser#PowExpr.
    def visitPowExpr(self, ctx:SolidityParser.PowExprContext):
        #lhs=expression op='**' rhs=expression
        str = self.visit(ctx.expression(0))+ " "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#StringLiteralExpr.
    def visitStringLiteralExpr(self, ctx:SolidityParser.StringLiteralExprContext):
        #StringLiteral
        str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#PlusMinusExpr.
    def visitPlusMinusExpr(self, ctx:SolidityParser.PlusMinusExprContext):
        #연산자 띄어쓰기
        #lhs=expression op=('+' | '-') rhs=expression
        #(2) (1)에서 @_t_x 를 붙인 인자에 대해 "사용"하는 것이 있으면 _reveal과 새로운 @_t_j 를 붙인다.(j는 새로운 숫자)
        res = ''
        namelist = self.name
        lex = self.visit(ctx.expression(0))
        rex = self.visit(ctx.expression(1))
        #파라미터 정보만 남게하기 위한 전처리
        tlex = self.removeReveal(lex)
        trex = self.removeReveal(rex)
        #parent 업데이트 유무
        isparent = False
        if len(self.parent) !=0:
            isparent = True
        for n in namelist:
            if n in tlex:
                self.addRelation(n)
                if isparent:
                    res +="_reveal("+lex+", @_t"+str(self.parent[self.count])
                else:
                    res +="_reveal("+lex+", @_t"+str(self.count)
                self.isUse = True#사용 유무 체크
                self.count += 1
            else:
                res += lex
            res += " " +ctx.getChild(1).__str__()+" "
            if n in trex:
                self.addRelation(n)
                if isparent:
                    res += "_reveal("+rex+", @_t"+str(self.parent[self.count])+")"
                else:
                    res += "_reveal("+rex+", @_t"+str(self.count)+")"
                self.isUse = True #사용 유무 체크
                self.count += 1
            else:
                res += rex
        # 원래 코드
        # res = self.visit(ctx.expression(0))+" " +ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return res

    #tlist에 인덱스 간의 관계 정보 추가
    def addRelation(self, var):
        if var in self.rindex and (self.rindex[var],self.count) not in self.tlist:#value확인, 중복 원소 확인
            self.tlist.append((self.rindex[var],self.count))
    #_reveal과 같은 문자열이 포함되어있는 경우 지우기
    def removeReveal(self, isReveal):
        result = isReveal
        if '_reveal' in isReveal:
            result = isReveal.replace('_reveal(', '')
        return result

    # Visit a parse tree produced by SolidityParser#CompExpr.
    def visitCompExpr(self, ctx:SolidityParser.CompExprContext):
        #연산자 띄어쓰기
        #lhs=expression op=('<' | '>' | '<=' | '>=') rhs=expression
        str = self.visit(ctx.expression(0))+" " +ctx.getChild(1).__str__()+" "+ self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#IndexExpr.
    def visitIndexExpr(self, ctx:SolidityParser.IndexExprContext):
        #arr=expression '[' index=expression ']'
        str = self.visit(ctx.expression(0))+ ctx.getChild(1).__str__()+ self.visit(ctx.expression(1))+ctx.getChild(3).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#SignExpr.
    def visitSignExpr(self, ctx:SolidityParser.SignExprContext):
        #op=('+' | '-') expr=expression
        str = ctx.getChild(0).__str__() + self.visit(ctx.expression())
        return str


    # Visit a parse tree produced by SolidityParser#NumberLiteralExpr.
    def visitNumberLiteralExpr(self, ctx:SolidityParser.NumberLiteralExprContext):
        # numberLiteral
        str = ctx.numberLiteral().getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#BitwiseNotExpr.
    def visitBitwiseNotExpr(self, ctx:SolidityParser.BitwiseNotExprContext):
        # '~' expr=expression
        str = ctx.getChild(0).__str__() + self.visit(ctx.expression())
        return str


    # Visit a parse tree produced by SolidityParser#IdentifierExpr.
    def visitIdentifierExpr(self, ctx:SolidityParser.IdentifierExprContext):
        # idf=identifier
        str = self.visitIdentifier(ctx.identifier())
        return str



    # Visit a parse tree produced by SolidityParser#BooleanLiteralExpr.
    def visitBooleanLiteralExpr(self, ctx:SolidityParser.BooleanLiteralExprContext):
        # BooleanLiteral
        str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#MeExpr.
    def visitMeExpr(self, ctx:SolidityParser.MeExprContext):
        # MeKeyword
        str = ctx.MeKeyword().__str__()
        return str


    # Visit a parse tree produced by SolidityParser#NotExpr.
    def visitNotExpr(self, ctx:SolidityParser.NotExprContext):
        # '!' expr=expression
        str = ctx.getChild(0).__str__() + self.visit(ctx.expression())
        return str


    # Visit a parse tree produced by SolidityParser#BitShiftExpr.
    def visitBitShiftExpr(self, ctx:SolidityParser.BitShiftExprContext):
        # lhs=expression op=('<<' | '>>') rhs=expression
        str = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#BitwiseAndExpr.
    def visitBitwiseAndExpr(self, ctx:SolidityParser.BitwiseAndExprContext):
        #  lhs=expression op='&' rhs=expression
        str = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#MultDivModExpr.
    def visitMultDivModExpr(self, ctx:SolidityParser.MultDivModExprContext):
        # lhs=expression op=('*' | '/' | '%') rhs=expression
        str = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#AssignmentExpr.
    def visitAssignmentExpr(self, ctx:SolidityParser.AssignmentExprContext):
        # lhs=expression op=('=' | '|=' | '^=' | '&=' | '<<=' | '>>=' | '+=' | '-=' | '*=' | '/=' | '%=') rhs=expression
        res=''
        #(2) (1)에서 @_t_x 를 붙인 인자에 대해 "사용"하는 것이 있으면 _reveal과 새로운 @_t_j 를 붙인다.(j는 새로운 숫자)
        namelist = self.name+self.cname
        rex = self.visit(ctx.expression(1))

        #reveal 위치 찾기
        rstart = rex.find("_reveal(")
        rend = rex.find("@")

        #trex = self.removeReveal(rex)
        flag = True
        isparent  = False
        if len(self.parent) !=0:
            isparent = True
        for n in namelist:
            nfind = rex.find(n)
            #해당 변수를 찾지 못하면 다른 변수 탐색
            if nfind == -1:
                continue
            #_reveal이 없으면, 평소대로 _reveal추가
            elif rstart == -1 and rend == -1:
                self.addRelation(n)
                res = self.visit(ctx.expression(0))
                for i in self.isMapping:
                    if i in res:
                        for j in range(len(res)):
                            if res[j] =="[":
                                index = j
                                break
                temp = res[:index]
                #두번 파싱하는 경우 기존에 업데이트되지 않은 튜플은 삭제함
                for i in self.tlist:
                    if i[0] == self.rindex[temp]:
                        self.tlist.remove(i)
                self.addRelation(temp)
                if isparent:
                    pc = self.parent[self.count]
                    if pc == 0 or pc == 1:
                        res += " "+ctx.getChild(1).__str__()+" _reveal("+rex+", @_t"+str(self.count)+")"
                    else:
                        res += " "+ctx.getChild(1).__str__()+" _reveal("+rex+", @_t"+str(self.parent[self.count])+")"
                else:
                    res += " "+ctx.getChild(1).__str__()+" _reveal("+rex+", @_t"+str(self.count)+")"
                self.count += 1
                self.isUse = True#사용 유무 체크
                flag = False
            # reveal 사이의 변수가 아니라면, _reveal 추가
            elif not (nfind > rstart and nfind < rend):
                #두번 파싱하는 경우 기존에 업데이트되지 않은 튜플은 삭제함
                for i in self.tlist:
                    if i[0] == self.rindex[n]:
                        self.tlist.remove(i)
                #동일한 의미를 가진 변수가 있나 확인해야함
                self.addRelation(n)
                if isparent:
                    pc = self.parent[self.count]
                    if pc ==0 or pc ==1:# me/all일경우 기존 번호 태깅
                        res = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" _reveal("+rex+", @_t"+str(self.count)+")"
                    else:
                        res = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" _reveal("+rex+", @_t"+str(pc)+")"
                else:
                    res = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" _reveal("+rex+", @_t"+str(self.count)+")"
                self.count += 1
                self.isUse = True#사용 유무 체크
                flag = False
        #위의 조건에 충족하지 않으면 아무 표시 추가하지 않음
        if flag:
            res = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return res


    # Visit a parse tree produced by SolidityParser#TupleExpr.
    def visitTupleExpr(self, ctx:SolidityParser.TupleExprContext):
        # expr=tupleExpression
        str = self.visitTupleExpression(ctx.tupleExpression())
        return str


    # Visit a parse tree produced by SolidityParser#OrExpr.
    def visitOrExpr(self, ctx:SolidityParser.OrExprContext):
        # lhs=expression op='||' rhs=expression
        str = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str

    # Visit a parse tree produced by SolidityParser#FunctionCallExpr.
    def visitFunctionCallExpr(self, ctx:SolidityParser.FunctionCallExprContext):
        # func=expression '(' args=functionCallArguments ')'
        fa = self.visitFunctionCallArguments(ctx.functionCallArguments())
        res = ''
        flag = True
        namelist = self.name
        #parent 업데이트 유무 확인
        isparent = False
        if len(self.parent) != 0:
            isparent = True
        #파라미터 정보만 남게하기 위한 전처리
        tfa = self.removeReveal(fa)
        for n in namelist:
            if n in tfa:
                #require문 특성상 reveal 대상은 all
                res = self.visit(ctx.expression())
                if res == "require":
                    #중복 원소 처리
                    if (0, self.count) not in self.tlist:
                        self.tlist.append((0,self.count))
                if isparent:
                    pc = self.parent[self.count]
                    if pc == 0 or pc == 1:
                        res += ctx.getChild(1).__str__()+"_reveal("+fa+", @_t"+str(self.count)+")"+ctx.getChild(3).__str__()
                    else:
                        res += ctx.getChild(1).__str__()+"_reveal("+fa+", @_t"+str(pc)+")"+ctx.getChild(3).__str__()
                else:
                    res += ctx.getChild(1).__str__()+"_reveal("+fa+", @_t"+str(self.count)+")"+ctx.getChild(3).__str__()
                self.isUse = True
                self.count += 1
                flag = False

        if flag:
            falist = fa.split("==")
            if falist[1] ==" me":#require에 ==me를 가지고 있으면
                res = self.visit(ctx.expression())
                #me와 같은 변수와 현재 함수 인덱스 정보 추가
                if (falist[0].rstrip(), self.fcnt) not in self.stlist:#중복 원소 처리
                    self.stlist.append((falist[0].rstrip(), self.fcnt))
                res += ctx.getChild(1).__str__()+fa+ctx.getChild(3).__str__()
            else:
                res = self.visit(ctx.expression())+fa+ctx.getChild(3).__str__()

        return res


    # Visit a parse tree produced by SolidityParser#EqExpr.
    def visitEqExpr(self, ctx:SolidityParser.EqExprContext):
        # lhs=expression op=('==' | '!=') rhs=expression
        str = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#PostCrementExpr.
    def visitPostCrementExpr(self, ctx:SolidityParser.PostCrementExprContext):
        # expr=expression op=('++' | '--')
        str = self.visit(ctx.expression())+ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#PrimitiveCastExpr.
    def visitPrimitiveCastExpr(self, ctx:SolidityParser.PrimitiveCastExprContext):
        # elem_type=elementaryTypeName '(' expr=expression ')'
        str = self.visitElementaryTypeName(ctx.elementaryTypeName())+ctx.getChild(1).__str__()+self.visit(ctx.expression())+ctx.getChild(3).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#BitwiseXorExpr.
    def visitBitwiseXorExpr(self, ctx:SolidityParser.BitwiseXorExprContext):
        # lhs=expression op='^' rhs=expression
        str = self.visit(ctx.expression(0))+ctx.getChild(1).__str__()+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#MemberAccessExpr.
    def visitMemberAccessExpr(self, ctx:SolidityParser.MemberAccessExprContext):
        # expr=expression '.' member=identifier
        str = self.visit(ctx.expression())+ctx.getChild(1).__str__()+self.visitIdentifier(ctx.identifier())
        return str


    # Visit a parse tree produced by SolidityParser#PreCrementExpr.
    def visitPreCrementExpr(self, ctx:SolidityParser.PreCrementExprContext):
        # op=('++' | '--') expr=expression
        str = ctx.getChild(0).__str__()+self.visit(ctx.expression())
        return str


    # Visit a parse tree produced by SolidityParser#functionCallArguments.
    def visitFunctionCallArguments(self, ctx:SolidityParser.FunctionCallArgumentsContext):
        #원본 (exprs+=expression (',' exprs+=expression)*)?

        if ctx.getChildCount()>0:
            res =self.visit(ctx.expression(0))
            for i in range(1, ctx.getChildCount(),2):
                res += ctx.getChild(i).__str__() + " "+ self.visit(ctx.getChild(i+1))
        else:
            res =""
        return res


    # Visit a parse tree produced by SolidityParser#tupleExpression.
    def visitTupleExpression(self, ctx:SolidityParser.TupleExpressionContext):
        #원본 '(' ( expression? ( ',' expression? )* ) ')'
        str = ctx.getChild(0).__str__()
        tp = ""
        if ctx.getChildCount()>2:
            for i in range(1, ctx.getChildCount()-1):
                if ctx.getChild(i).__str__().__eq__(","):
                    tp+= ctx.getChild(i).__str__()
                else :
                    tp+= self.visit(ctx.getChild(i))
            str += tp + ctx.getChild(ctx.getChildCount()-1).__str__()
        # '(' ')'
        else:
            str +=ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#elementaryTypeNameExpression.
    def visitElementaryTypeNameExpression(self, ctx:SolidityParser.ElementaryTypeNameExpressionContext):
        str = ctx.elementaryTypeName().__str__()
        return str


    # Visit a parse tree produced by SolidityParser#numberLiteral.
    def visitNumberLiteral(self, ctx:SolidityParser.NumberLiteralContext):
        str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#annotatedTypeName.
    def visitAnnotatedTypeName(self, ctx:SolidityParser.AnnotatedTypeNameContext):
        # type_name=typeName ('@' privacy_annotation=expression)?
        str = self.visitTypeName(ctx.typeName())
        if ctx.getChildCount()>1:
            str += ctx.getChild(1).__str__()+ self.visit(ctx.expression())
        return str

    # Visit a parse tree produced by SolidityParser#identifier.
    def visitIdentifier(self, ctx:SolidityParser.IdentifierContext):
        # IdentifierStart IdentifierPart*
        str =ctx.getChild(0).__str__()
        if ctx.getChildCount()>1:
            for i in range(1, ctx.getChildCount()-1):
                str +=ctx.getChild(i).__str__()
        return str